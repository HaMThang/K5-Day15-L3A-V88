"""Xuất `slides/slides.html` thành `demo-slides.pdf` ở thư mục gốc repo bằng trình duyệt Edge/Chrome headless có sẵn trên máy.

Chạy bằng:
    python slides/build_pdf.py
Chỉ dùng thư viện chuẩn của Python 3.10+.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "slides" / "slides.html"
PDF_PATH = ROOT / "demo-slides.pdf"

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    shutil.which("msedge") or "",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def find_browser() -> str | None:
    for cand in BROWSER_CANDIDATES:
        if cand and os.path.exists(cand):
            return cand
    return None


def main() -> int:
    if not HTML_PATH.exists():
        print(f"Không tìm thấy {HTML_PATH}", file=sys.stderr)
        return 1
    browser = find_browser()
    if not browser:
        print("Không tìm thấy Microsoft Edge hoặc Google Chrome để xuất PDF.", file=sys.stderr)
        return 1

    uri = HTML_PATH.as_uri()
    with tempfile.TemporaryDirectory(prefix="v88_slides_") as profile_dir:
        cmd = [
            browser,
            "--headless=new",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_PATH}",
            uri,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=25)

    if proc.returncode != 0 or not PDF_PATH.exists():
        print(f"Lỗi xuất PDF (code={proc.returncode}): {proc.stderr[:400]}", file=sys.stderr)
        return 1

    size_kb = PDF_PATH.stat().st_size / 1024.0
    print(f"Đã xuất thành công: {PDF_PATH} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
