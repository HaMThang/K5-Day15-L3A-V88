"""Giao diện CLI (`python run.py`) và Web cục bộ (`python codebase/app.py --web`) — Nhóm V88."""
import base64
import json
import os
import re
import secrets
import shutil
import sys
import tempfile
import time
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_MODE_CMDS = {
    "/1": "giai_thich",
    "/mode 1": "giai_thich",
    "/mode giai_thich": "giai_thich",
    "/2": "goi_y",
    "/mode 2": "goi_y",
    "/mode goi_y": "goi_y",
    "/3": "cam_tay",
    "/mode 3": "cam_tay",
    "/mode cam_tay": "cam_tay",
}


def _where(e: BaseException) -> str:
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path


def main() -> int:
    try:
        import tracing
        from agent import MODE_LABELS, answer
    except Exception as e:
        print(f"Không nạp được codebase/ — lỗi ở {_where(e)}: {type(e).__name__}: {e}")
        print("Xem cách nối model tại docs/connect-model.md")
        return 1

    current_mode = (os.environ.get("GUIDANCE_MODE") or "goi_y").strip().lower()
    if current_mode not in MODE_LABELS:
        current_mode = "goi_y"
    repo_path = (os.environ.get("LAB_REPO_PATH") or "").strip()

    print("=== Lab Compass · Trợ lý bài Lab L3 (Nhóm V88) ===")
    print("Chỉ đọc tài liệu & mã nguồn để hướng dẫn; không viết code hộ, không cài môi trường, không chạy lệnh.")
    print("Lệnh nhanh: `/1` Giải thích · `/2` Gợi ý · `/3` Cầm tay chỉ việc · `/repo <đường_dẫn>` gắn thư mục lab.")
    print("Thoát: Ctrl+C hoặc nhấn Enter 2 lần.\n")

    blank = 0
    while True:
        repo_label = os.path.basename(repo_path.rstrip("\\/")) if (repo_path and os.path.isdir(repo_path)) else "kb_index"
        try:
            text = input(f"[{current_mode} | {repo_label}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0

        low = text.lower()
        if low in _MODE_CMDS:
            current_mode = _MODE_CMDS[low]
            print(f"-> Chế độ: {MODE_LABELS[current_mode]}")
            continue
        if low.startswith("/repo"):
            arg = text[5:].strip().strip('"').strip("'")
            if not arg:
                repo_path = ""
                print("-> Đã quay về dùng chỉ mục `data/kb_index.json`.")
            elif os.path.isdir(arg):
                repo_path = os.path.abspath(arg)
                print(f"-> Đã gắn thư mục bài lab: {repo_path}")
            else:
                print(f"[!] Không tìm thấy thư mục: {arg}")
            continue

        tracing.begin("app")
        try:
            result = answer(text, mode=current_mode, repo_path=repo_path if os.path.isdir(repo_path) else "")
        except NotImplementedError as e:
            tracing.end()
            print(f"Chưa nối model: {e}")
            return 1
        except Exception as e:
            tracing.end()
            print(f"[lỗi] {type(e).__name__}: {e}")
            continue
        s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        models = ", ".join(s["models"]) or "—"
        print(f"   (model: {models} · gọi model {s['model_calls']} · công cụ {s['tool_calls']} · token vào {s['tokens_in']} / ra {s['tokens_out']})")


def serve_web() -> int:
    import tracing
    from agent import MODE_LABELS, answer

    # Local: không đặt biến nào -> giữ nguyên 127.0.0.1:8000 như trước.
    # Render: đặt HOST=0.0.0.0, PUBLIC_ORIGIN=https://<tên>.onrender.com; Render tự cấp PORT.
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    public_origin = os.environ.get("PUBLIC_ORIGIN", "").strip().rstrip("/")
    address = public_origin.split("://", 1)[-1] if public_origin else f"127.0.0.1:{port}"
    origin = public_origin or f"http://{address}"
    # Bản công khai không cho đọc thư mục trên server (repo_path) và giới hạn lượt hỏi để giữ chi phí.
    allow_repo = not public_origin
    per_ip_limit = int(os.environ.get("RATE_LIMIT_PER_HOUR", "0"))
    daily_limit = int(os.environ.get("RATE_LIMIT_PER_DAY", "0"))
    hits: dict[str, list[float]] = {}
    day_hits: list[float] = []

    def over_limit(ip: str) -> bool:
        now = time.time()
        if per_ip_limit:
            recent = [t for t in hits.get(ip, []) if now - t < 3600]
            hits[ip] = recent
            if len(recent) >= per_ip_limit:
                return True
        if daily_limit:
            day_hits[:] = [t for t in day_hits if now - t < 86400]
            if len(day_hits) >= daily_limit:
                return True
        hits.setdefault(ip, []).append(now)
        day_hits.append(now)
        return False

    # Thư mục lab chọn từ trình duyệt: lưu tạm trên server, mỗi lần chọn một thư mục riêng, tự xoá sau 1 giờ.
    import tools

    upload_root = Path(tempfile.mkdtemp(prefix="labcompass-"))
    uploads: dict[str, tuple[float, str]] = {}
    upload_hits: dict[str, list[float]] = {}
    upload_ttl, max_uploads, max_upload_bytes = 3600, 30, 4_000_000

    def drop_upload(lab_id: str) -> None:
        _, path = uploads.pop(lab_id, (0.0, ""))
        if path:
            tools._REPO_CACHE.pop(os.path.abspath(path), None)
            shutil.rmtree(os.path.dirname(path), ignore_errors=True)

    def prune_uploads() -> None:
        now = time.time()
        for lab_id, (created, _) in list(uploads.items()):
            if now - created > upload_ttl:
                drop_upload(lab_id)
        for lab_id, _ in sorted(uploads.items(), key=lambda kv: kv[1][0])[: max(0, len(uploads) - max_uploads + 1)]:
            drop_upload(lab_id)

    def safe_parts(rel: str) -> list[str] | None:
        parts = rel.replace("\\", "/").split("/")
        if any(p in ("", ".", "..") or ":" in p for p in parts):
            return None
        if any(d in tools._SKIP_DIRS or d.startswith(".") for d in parts[:-1]):
            return None
        name = parts[-1]
        if os.path.splitext(name)[1].lower() not in tools._ALLOWED_EXTS or tools._is_secret_filename(name):
            return None
        return parts

    def save_upload(name: str, files: list) -> tuple[str, str, int, int]:
        prune_uploads()
        lab_id = secrets.token_urlsafe(12)
        folder = re.sub(r"[^\w.-]", "_", name)[:80].strip("._") or "lab"
        lab_dir = (upload_root / lab_id / folder).resolve()
        lab_dir.mkdir(parents=True)
        saved = skipped = 0
        for item in files:
            parts = safe_parts(item.get("path", "")) if isinstance(item, dict) else None
            # Trình duyệt gửi nội dung dạng base64: tường lửa của Render chặn request chứa mã nguồn thô.
            encoded = item.get("content_b64") if parts else None
            if not parts or not isinstance(encoded, str) or saved >= tools._MAX_SCAN_FILES:
                skipped += 1
                continue
            try:
                data = base64.b64decode(encoded, validate=True)
                data.decode("utf-8")
            except ValueError:
                skipped += 1
                continue
            dest = lab_dir.joinpath(*parts).resolve()
            if len(data) > tools._MAX_FILE_BYTES or not str(dest).startswith(str(lab_dir) + os.sep):
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            saved += 1
        if not saved:
            shutil.rmtree(lab_dir.parent, ignore_errors=True)
            raise ValueError
        uploads[lab_id] = (time.time(), str(lab_dir))
        return lab_id, folder, saved, skipped

    def upload_limited(ip: str) -> bool:
        now = time.time()
        recent = [t for t in upload_hits.get(ip, []) if now - t < 3600]
        upload_hits[ip] = recent + [now]
        return len(recent) >= 20

    assets = {
        "/": ("index.html", "text/html"),
        "/app.js": ("app.js", "text/javascript"),
        "/style.css": ("style.css", "text/css"),
    }
    web_root = Path(__file__).resolve().with_name("web")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:
            return

        def send_body(self, code: int, content_type: str, body: bytes) -> None:
            self.send_response(code)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, code: int, data: dict) -> None:
            self.send_body(code, "application/json", json.dumps(data).encode("utf-8"))

        def do_GET(self) -> None:
            if self.path == "/healthz":
                self.send_body(200, "text/plain", b"ok")
                return
            if self.path == "/api/config" and self.headers.get("Host") == address:
                self.send_json(200, {"allow_repo_path": allow_repo, "upload_ttl_minutes": upload_ttl // 60,
                                     "max_files": tools._MAX_SCAN_FILES, "max_file_bytes": tools._MAX_FILE_BYTES})
                return
            if self.headers.get("Host") != address or self.path not in assets:
                self.send_error(404)
                return
            name, mime = assets[self.path]
            self.send_body(200, mime, (web_root / name).read_bytes())

        def read_json(self, limit: int) -> dict:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= limit or self.headers.get_content_type() != "application/json":
                raise ValueError
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError
            return data

        def do_POST(self) -> None:
            if self.path not in ("/api/answer", "/api/upload_lab"):
                self.send_json(404, {"error": "Không tìm thấy đường dẫn."})
                return
            if self.headers.get("Host") != address or self.headers.get("Origin") != origin:
                self.send_json(403, {"error": "Hãy gửi câu hỏi từ giao diện Lab Compass."})
                return
            forwarded = self.headers.get("X-Forwarded-For", "")
            client_ip = forwarded.split(",")[0].strip() if public_origin and forwarded else self.client_address[0]
            if self.path == "/api/upload_lab":
                self.handle_upload(client_ip)
                return
            if over_limit(client_ip):
                self.send_json(429, {"error": "Đã hết lượt hỏi thử, vui lòng quay lại sau."})
                return
            try:
                data = self.read_json(16384)
                question, mode, repo, lab_id = (data.get(k, "") for k in ("question", "mode", "repo_path", "lab_id"))
                if not all(isinstance(v, str) for v in (question, mode, repo, lab_id)):
                    raise ValueError
                if not 0 < len(question.strip()) <= 1500 or mode not in MODE_LABELS:
                    raise ValueError
            except ValueError:
                self.send_json(400, {"error": "Câu hỏi hoặc mức hướng dẫn không hợp lệ."})
                return

            repo = repo.strip()
            if lab_id:
                prune_uploads()
                if lab_id not in uploads:
                    self.send_json(410, {"error": "Thư mục lab đã chọn đã hết hạn, hãy chọn lại thư mục.", "lab_expired": True})
                    return
                repo = uploads[lab_id][1]
            elif repo and not allow_repo:
                self.send_json(400, {"error": "Bản dùng thử trực tuyến không đọc thư mục lab; hãy để trống đường dẫn."})
                return
            if repo and not lab_id and (repo.startswith(("\\\\", "//")) or not os.path.isdir(repo)):
                self.send_json(400, {"error": "Không tìm thấy thư mục lab trên máy này."})
                return

            tracing.begin("web")
            try:
                result = answer(question, mode=mode, repo_path=repo)
            except Exception as error:
                print(f"[web] {type(error).__name__}: {error}", file=sys.stderr)
                result = None
            finally:
                summary, _ = tracing.end()

            if result is None:
                self.send_json(500, {"error": "Không thể tra cứu lúc này. Xem chi tiết lỗi ở terminal."})
                return
            self.send_json(200, {
                "output": result["output"],
                "model": ", ".join(summary["models"]),
                **{k: summary[k] for k in ("model_calls", "tool_calls", "tokens_in", "tokens_out")},
            })

        def handle_upload(self, client_ip: str) -> None:
            if upload_limited(client_ip):
                self.send_json(429, {"error": "Bạn đã chọn thư mục quá nhiều lần, vui lòng thử lại sau."})
                return
            try:
                data = self.read_json(max_upload_bytes)
                name, files = data.get("name", ""), data.get("files")
                if not isinstance(name, str) or not isinstance(files, list) or not files:
                    raise ValueError
                lab_id, folder, saved, skipped = save_upload(name, files)
            except (ValueError, OSError):
                self.send_json(400, {"error": "Thư mục không có file tài liệu phù hợp (.md, .py, .yaml, .txt) hoặc quá lớn."})
                return
            self.send_json(200, {"lab_id": lab_id, "name": folder, "files": saved, "skipped": skipped,
                                 "ttl_minutes": upload_ttl // 60})

    # Render dừng server bằng SIGTERM: đổi thành thoát bình thường để khối finally dọn thư mục tạm.
    import signal
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        with HTTPServer((host, port), Handler) as server:
            print(f"Lab Compass · {origin} · Ctrl+C để thoát", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except OSError as error:
        print(f"Không mở được cổng Web UI: {error}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(upload_root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(serve_web() if sys.argv[1:] == ["--web"] else main())
