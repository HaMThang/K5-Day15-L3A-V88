"""Giao diện CLI (`python run.py`) và Web cục bộ (`python codebase/app.py --web`) — Nhóm V88."""
import json
import os
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
        from tools import resolve_lab_source
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
    print("Lệnh nhanh: `/1` Giải thích · `/2` Gợi ý · `/3` Cầm tay chỉ việc · `/repo <thư mục hoặc link GitHub>` gắn bài lab.")
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
            else:
                resolved, error = resolve_lab_source(arg)
                if error:
                    print(f"[!] {error}")
                else:
                    repo_path = resolved
                    print(f"-> Đã gắn bài lab: {arg}")
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


_SAVED_PATH = os.path.join(tempfile.gettempdir(), "lab_compass_saved_answers.json")


def _load_saved() -> dict:
    try:
        with open(_SAVED_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _save_result(key: str, value: dict) -> None:
    data = _load_saved()
    data[key] = value
    with open(_SAVED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def serve_web() -> int:
    import tracing
    from agent import MODE_LABELS, answer
    from tools import resolve_lab_source

    address = "127.0.0.1:8000"
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
            if self.headers.get("Host") != address or self.path not in assets:
                self.send_error(404)
                return
            name, mime = assets[self.path]
            self.send_body(200, mime, (web_root / name).read_bytes())

        def do_POST(self) -> None:
            if self.path != "/api/answer":
                self.send_json(404, {"error": "Không tìm thấy đường dẫn."})
                return
            if self.headers.get("Host") != address or self.headers.get("Origin") != f"http://{address}":
                self.send_json(403, {"error": "Hãy gửi câu hỏi từ giao diện Lab Compass."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16384 or self.headers.get_content_type() != "application/json":
                    raise ValueError
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError
                question, mode, repo = (data.get(k, "") for k in ("question", "mode", "repo_path"))
                if not all(isinstance(v, str) for v in (question, mode, repo)):
                    raise ValueError
                if not 0 < len(question.strip()) <= 1500 or mode not in MODE_LABELS:
                    raise ValueError
            except ValueError:
                self.send_json(400, {"error": "Câu hỏi hoặc mức hướng dẫn không hợp lệ."})
                return

            source_text = repo
            repo, error = resolve_lab_source(repo)
            if error:
                self.send_json(400, {"error": error})
                return

            # Kết quả đã lưu: chỉ là lần chạy model THẬT gần nhất cho đúng câu/mức/nguồn này,
            # trả kèm nhãn và giờ chạy; nút "Chạy lại trực tiếp" (live=true) luôn gọi model mới.
            key = "|".join((mode, source_text.strip().lower(), " ".join(question.lower().split())))
            saved = _load_saved().get(key)
            if saved and data.get("live") is not True:
                self.send_json(200, {**saved, "saved": True})
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
            reply = {
                "output": result["output"],
                "model": ", ".join(summary["models"]),
                **{k: summary[k] for k in ("model_calls", "tool_calls", "tokens_in", "tokens_out")},
            }
            if summary["model_calls"] and summary["tokens_out"]:  # chỉ lưu câu trả lời do model thật sinh ra
                _save_result(key, {**reply, "saved_at": time.strftime("%H:%M %d/%m")})
            self.send_json(200, {**reply, "saved": False})

    try:
        with HTTPServer(("127.0.0.1", 8000), Handler) as server:
            print(f"Lab Compass · http://{address} · Ctrl+C để thoát", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except OSError as error:
        print(f"Không mở được cổng Web UI: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(serve_web() if sys.argv[1:] == ["--web"] else main())
