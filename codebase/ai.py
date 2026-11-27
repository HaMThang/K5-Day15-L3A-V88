"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chỉ dùng thư viện chuẩn Python (`urllib.request`, `json`). Hỗ trợ:
    - fake       (mặc định trước CP3 khi chưa điền .env)
    - gemini     (Google AI Studio REST API)
    - openai     (OpenAI Chat Completions hoặc API tương thích qua API_BASE_URL: DeepSeek, Groq, OpenRouter)
    - anthropic  (Claude Messages API)
    - ollama     (Local Ollama server)
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path: str = os.path.join(ROOT, ".env")) -> None:
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
API_BASE_URL = (os.environ.get("API_BASE_URL") or "").strip()

_PROVIDER_DEFAULT_URLS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
}


def post_json(url: str, headers: dict[str, str], body: dict, timeout: int = 60, max_retries: int = 2) -> dict:
    """Gửi POST JSON bằng thư viện chuẩn urllib, có thử lại nhẹ khi gặp lỗi tạm thời (429 / 5xx)."""
    payload = json.dumps(body).encode("utf-8")
    req_headers = dict({"Content-Type": "application/json"}, **headers)
    last_err: Exception | None = None

    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=payload, method="POST", headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if SHOW_RAW:
                print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
            return data
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", "replace")[:350]
            last_err = RuntimeError("HTTP %d: %s" % (e.code, err_body))
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise last_err
        except urllib.error.URLError as e:
            last_err = RuntimeError("URLError: %s" % e.reason)
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise last_err

    raise last_err or RuntimeError("Không gọi được API model.")


def call_openai_compatible(system: str, user: str, url: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env cho nhà cung cấp %s." % MODEL_PROVIDER)
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env cho nhà cung cấp %s." % MODEL_PROVIDER)
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    body = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.1,
    }
    data = post_json(url, {"Authorization": "Bearer " + API_KEY}, body)
    usage = data.get("usage") or {}
    msg = (data.get("choices") or [{}])[0].get("message") or {}
    content = msg.get("content") or ""
    tokens_in = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
    tokens_out = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
    return {"text": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def call_gemini(system: str, user: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env cho MODEL_PROVIDER=gemini.")
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env cho MODEL_PROVIDER=gemini (vd: gemini-2.5-flash hoặc gemini-3.1-flash-lite).")
    model_slug = urllib.parse.quote(MODEL_NAME, safe="-._")
    url = API_BASE_URL or f"https://generativelanguage.googleapis.com/v1beta/models/{model_slug}:generateContent"
    body: dict = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.1},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {"x-goog-api-key": API_KEY}, body)
    candidates = data.get("candidates") or []
    parts = ((candidates[0].get("content") or {}).get("parts") or []) if candidates else []
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and not p.get("thought"))
    usage = data.get("usageMetadata") or {}
    tokens_in = int(usage.get("promptTokenCount") or 0)
    tokens_out = int(usage.get("candidatesTokenCount") or 0) + int(usage.get("thoughtsTokenCount") or 0)
    return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out}


def call_claude(system: str, user: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env cho MODEL_PROVIDER=anthropic.")
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env cho MODEL_PROVIDER=anthropic.")
    url = API_BASE_URL or "https://api.anthropic.com/v1/messages"
    body = {
        "model": MODEL_NAME,
        "max_tokens": 2048,
        "system": system or "",
        "messages": [{"role": "user", "content": user}],
    }
    data = post_json(url, {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"}, body)
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    usage = data.get("usage") or {}
    return {
        "text": text,
        "tokens_in": int(usage.get("input_tokens") or 0),
        "tokens_out": int(usage.get("output_tokens") or 0),
    }


def call_ollama(system: str, user: str) -> dict:
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env cho MODEL_PROVIDER=ollama.")
    url = API_BASE_URL or "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": (data.get("message") or {}).get("content", ""),
        "tokens_in": int(data.get("prompt_eval_count") or 0),
        "tokens_out": int(data.get("eval_count") or 0),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if not MODEL_PROVIDER or MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:60],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }

    if MODEL_PROVIDER in _PROVIDER_DEFAULT_URLS:
        url = API_BASE_URL or _PROVIDER_DEFAULT_URLS[MODEL_PROVIDER]
        r = call_openai_compatible(system, user, url)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Chưa hỗ trợ MODEL_PROVIDER=%r trong codebase/ai.py (chọn fake, gemini, openai, deepseek, groq, openrouter, anthropic, hoặc ollama)."
            % MODEL_PROVIDER
        )

    return {
        "text": str(r["text"]),
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
