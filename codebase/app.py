"""Giao diện CLI tương tác của bản chạy thử MVP — Nhóm V88.

Cho phép học viên:
  1. Gắn đường dẫn thư mục bài Lab vừa fork/clone (`/repo <đường_dẫn>`, hoặc biến môi trường LAB_REPO_PATH)
     để trợ lý đọc tĩnh toàn bộ cấu trúc codebase (100% Read-Only: không cài môi trường, không chạy lệnh, không sửa file).
  2. Chọn ngay 1 trong 3 mức hướng dẫn sư phạm:
     - `/1` hoặc `/mode giai_thich` : Giải thích bản chất & tại sao cần bước đó
     - `/2` hoặc `/mode goi_y`      : Gợi ý định hướng Socratic (mặc định)
     - `/3` hoặc `/mode cam_tay`    : Cầm tay chỉ việc từng bước & hướng dẫn tự sửa lỗi (không viết full code)

Chạy bằng: python run.py
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _where(e: BaseException) -> str:
    import traceback
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
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1

    current_mode = (os.environ.get("GUIDANCE_MODE") or "goi_y").strip().lower()
    if current_mode not in MODE_LABELS:
        current_mode = "goi_y"
    repo_path = (os.environ.get("LAB_REPO_PATH") or "").strip()

    print("=== Trợ lý Hướng dẫn Bài Lab L3 (Nhóm V88 · Read-Only · Hiểu bản chất & Tự tay làm) ===")
    print("Ranh giới an toàn: Chỉ đọc codebase để dẫn dắt; KHÔNG viết full code, KHÔNG tự setup môi trường, KHÔNG chạy lệnh.")
    print("Lệnh nhanh: `/1` Giải thích · `/2` Gợi ý (mặc định) · `/3` Cầm tay chỉ việc · `/repo <đường_dẫn_lab>` gắn bài lab vừa clone.")
    print("Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).\n")

    blank = 0
    while True:
        repo_label = os.path.basename(repo_path.rstrip("\\/")) if (repo_path and os.path.isdir(repo_path)) else "kb_index (12 Lab K5)"
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
        if low in ("/1", "/mode 1", "/mode giai_thich"):
            current_mode = "giai_thich"
            print(f"-> Đã chuyển sang chế độ: {MODE_LABELS[current_mode]}")
            continue
        if low in ("/2", "/mode 2", "/mode goi_y"):
            current_mode = "goi_y"
            print(f"-> Đã chuyển sang chế độ: {MODE_LABELS[current_mode]}")
            continue
        if low in ("/3", "/mode 3", "/mode cam_tay"):
            current_mode = "cam_tay"
            print(f"-> Đã chuyển sang chế độ: {MODE_LABELS[current_mode]}")
            continue
        if low.startswith("/repo"):
            arg = text[5:].strip().strip('"').strip("'")
            if not arg:
                repo_path = ""
                print("-> Đã quay về dùng chỉ mục chuẩn `data/kb_index.json`.")
            elif os.path.isdir(arg):
                repo_path = os.path.abspath(arg)
                print(f"-> Đã nạp (Read-Only) thư mục bài lab: {repo_path}")
            else:
                print(f"[!] Không tìm thấy thư mục: {arg}")
            continue

        prefix = f"[mode={current_mode}]"
        if repo_path and os.path.isdir(repo_path):
            prefix += f" [repo={repo_path}]"
        payload = f"{prefix} {text}"

        tracing.begin("app")
        try:
            result = answer(payload)
        except NotImplementedError as e:
            tracing.end()
            print("Chưa nối model: %s" % e)
            return 1
        except Exception as e:
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


if __name__ == "__main__":
    sys.exit(main())
