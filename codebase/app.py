"""Giao diện web cục bộ cho workflow tra cứu; chạy bằng python run.py."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import webbrowser

import tracing
from agent import MAX_INPUT_CHARS, answer
from ai import MODEL_PROVIDER

STATIC = Path(__file__).resolve().parent / "web"
HOST = "127.0.0.1"
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def _json(self, status: int, data: dict) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        files = {"/": ("index.html", "text/html"), "/style.css": ("style.css", "text/css"),
                 "/app.js": ("app.js", "application/javascript")}
        route = files.get(urlsplit(self.path).path)
        if route is None:
            self.send_error(404)
            return
        self._send(200, (STATIC / route[0]).read_bytes(), route[1] + "; charset=utf-8")

    def do_POST(self) -> None:
        if self.path != "/api/answer":
            self.send_error(404)
            return
        origin = self.headers.get("Origin", "")
        if origin != f"http://{HOST}:{PORT}" or self.headers.get("Host") != f"{HOST}:{PORT}":
            self._json(403, {"error": "Yêu cầu không hợp lệ."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16000:
                raise ValueError
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = payload.get("question") if isinstance(payload, dict) else None
            if not isinstance(question, str) or not question.strip() or len(question) > MAX_INPUT_CHARS:
                raise ValueError
            previous = payload.get("previous_question", "")
            if not isinstance(previous, str) or len(previous) > MAX_INPUT_CHARS:
                raise ValueError
        except (ValueError, UnicodeError, json.JSONDecodeError):
            self._json(400, {"error": "Nhập câu hỏi từ 1 đến 1500 ký tự."})
            return
        tracing.begin("app")
        try:
            # Chỉ dùng câu hỏi trước của học viên, không đưa câu trả lời model cũ
            # vào nguồn. Luôn giữ nguyên câu hỏi mới trong giới hạn của agent.
            prefix = "Câu hỏi trước của học viên: "
            separator = "\nCâu hỏi hiện tại: "
            room = MAX_INPUT_CHARS - len(question) - len(prefix) - len(separator)
            context = previous[:min(500, max(0, room))].strip()
            combined = f"{prefix}{context}{separator}{question}" if context else question
            result = answer(combined)
            summary, _ = tracing.end()
            self._json(200, {"output": result["output"], "model": ", ".join(summary["models"]),
                             "fake": MODEL_PROVIDER in ("", "fake")})
        except Exception as exc:
            tracing.note("Lỗi xử lý: " + type(exc).__name__)
            tracing.end()
            print("Lỗi xử lý yêu cầu: " + type(exc).__name__, flush=True)
            self._json(502, {"error": "Không thể kết nối hoặc xử lý câu trả lời. Hãy kiểm tra cấu hình model và kết nối mạng rồi thử lại."})


def main() -> int:
    try:
        server = HTTPServer((HOST, PORT), Handler)
    except OSError as exc:
        print(f"Không mở được http://{HOST}:{PORT}: {exc}")
        return 1
    url = f"http://{HOST}:{PORT}"
    print(f"Trợ lý Lab đang chạy tại {url} · Dừng bằng Ctrl+C", flush=True)
    if MODEL_PROVIDER in ("", "fake"):
        print("Lưu ý: đang dùng model giả; kiểm tra .env để kết nối model thật.", flush=True)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
