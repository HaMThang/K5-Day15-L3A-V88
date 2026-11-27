"""Công cụ của bài toán — Nhóm V88 (Track A · Trợ lý tra cứu yêu cầu bài Lab hàng ngày lớp L3).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý khớp sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không.
Chỉ dùng thư viện chuẩn của Python 3.10+. Dữ liệu đọc từ `data/kb_index.json` (mô tả ở `data/DATA_CARD.md`).
"""
from __future__ import annotations

import json
import math
import os
import re
import unicodedata
from typing import Any

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "data", "kb_index.json")

_STOPWORDS = {
    "la", "va", "cua", "cho", "trong", "co", "khong", "duoc", "nhung", "cac", "mot",
    "nhu", "the", "nao", "gi", "o", "tai", "voi", "khi", "thi", "de", "ra", "vao",
    "len", "xuong", "hay", "hoac", "neu", "ma", "da", "dang", "se", "can", "phai",
    "minh", "nhom", "ban", "em", "anh", "chi", "oi", "nhe", "a", "ha", "vay", "chua",
    "bai", "ngay", "lop",
}

_CACHE: dict[str, Any] | None = None


def _strip_accents(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _normalize_day_mentions(folded: str) -> str:
    """Chuẩn hoá 'day 6', 'day6', 'lab 6', 'ngay 6' -> thêm token chuẩn 'day06' để khớp K5-Day06."""
    extras: list[str] = []
    for m in re.finditer(r"\b(?:day|lab|ngay)\s*[-_]?0?(\d{1,2})\b", folded):
        num = int(m.group(1))
        if 1 <= num <= 30:
            extras.append(f"day{num:02d}")
    return folded + (" " + " ".join(extras) if extras else "")


def _tokenize(text: str) -> list[str]:
    folded = _normalize_day_mentions(_strip_accents(text.lower()))
    raw_tokens = re.findall(r"[a-z0-9_#.\-/]+", folded)
    tokens: list[str] = []
    for raw in raw_tokens:
        for tok in re.split(r"[/#]", raw):
            tok = tok.strip(".-_")
            if not tok:
                continue
            if tok in _STOPWORDS and len(tok) <= 4:
                continue
            tokens.append(tok)
    return tokens


def _load_kb() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    if not os.path.exists(INDEX_PATH):
        _CACHE = {"version": "unknown", "sections": [], "by_code": {}, "idf": {}, "avgdl": 1.0, "doc_tokens": []}
        return _CACHE

    with open(INDEX_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    sections: list[dict[str, Any]] = raw.get("sections", [])
    by_code = {s["code"].lower(): s for s in sections}

    doc_tokens: list[list[str]] = []
    df: dict[str, int] = {}
    for sec in sections:
        weighted_text = " ".join([
            sec.get("code", ""),
            sec.get("lab", ""),
            sec.get("title", ""),
            sec.get("title", ""),
            " ".join(sec.get("keywords", [])),
            " ".join(sec.get("keywords", [])),
            sec.get("summary", ""),
            sec.get("quote", ""),
            sec.get("file", ""),
        ])
        toks = _tokenize(weighted_text)
        doc_tokens.append(toks)
        for u in set(toks):
            df[u] = df.get(u, 0) + 1

    n_docs = max(len(sections), 1)
    avgdl = sum(len(t) for t in doc_tokens) / n_docs
    idf = {term: math.log(1.0 + (n_docs - freq + 0.5) / (freq + 0.5)) for term, freq in df.items()}

    _CACHE = {
        "version": raw.get("version", "K5-L3-Phase1-Labs"),
        "updated_at": raw.get("updated_at", ""),
        "sections": sections,
        "by_code": by_code,
        "doc_tokens": doc_tokens,
        "idf": idf,
        "avgdl": max(avgdl, 1.0),
    }
    return _CACHE


@tool
def search_docs(query: str, k: int = 5) -> list:
    """Tên: search_docs — Tra cứu các mục hướng dẫn bài Lab L3 K5 theo BM25 và tự kéo kèm mục đối chiếu nếu 2 file lệch nhau.
    Input: query (str) — câu hỏi của học viên; k (int, mặc định 5) — số đoạn tối đa.
    Output: danh sách dict {"code", "lab", "file", "title", "summary", "quote", "version", "score", "conflicts_with"}.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu cục bộ từ data/kb_index.json)."""
    kb = _load_kb()
    sections = kb["sections"]
    if not sections or not query or not query.strip():
        return []

    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    q_folded = _normalize_day_mentions(_strip_accents(query.lower()))
    idf = kb["idf"]
    avgdl = kb["avgdl"]
    k1, b = 1.5, 0.75

    scored: list[tuple[float, dict[str, Any]]] = []
    for sec, d_toks in zip(sections, kb["doc_tokens"]):
        if not d_toks:
            continue
        dl = len(d_toks)
        tf_map: dict[str, int] = {}
        for t in d_toks:
            tf_map[t] = tf_map.get(t, 0) + 1

        score = 0.0
        for qt in q_tokens:
            tf = tf_map.get(qt, 0)
            if tf == 0:
                continue
            term_idf = idf.get(qt, 0.5)
            score += term_idf * (tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * dl / avgdl))

        for kw in sec.get("keywords", []):
            kw_f = _strip_accents(kw.lower()).strip()
            if kw_f and len(kw_f) >= 3 and kw_f in q_folded:
                score += 2.2

        if score > 0.0:
            scored.append((score, sec))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_k = max(1, min(int(k), 8))
    picked: list[dict[str, Any]] = []
    seen_codes: set[str] = set()

    for score, sec in scored[:top_k]:
        code = sec["code"]
        seen_codes.add(code.lower())
        picked.append({
            "code": code,
            "lab": sec.get("lab", ""),
            "file": sec.get("file", ""),
            "title": sec["title"],
            "summary": sec["summary"],
            "quote": sec["quote"],
            "version": kb["version"],
            "score": round(score, 3),
            "conflicts_with": list(sec.get("conflicts_with", [])),
        })

    for item in list(picked[:2]):
        for conflict_code in item.get("conflicts_with", []):
            c_key = conflict_code.lower()
            if c_key not in seen_codes and c_key in kb["by_code"]:
                c_sec = kb["by_code"][c_key]
                seen_codes.add(c_key)
                picked.append({
                    "code": c_sec["code"],
                    "lab": c_sec.get("lab", ""),
                    "file": c_sec.get("file", ""),
                    "title": c_sec["title"],
                    "summary": c_sec["summary"],
                    "quote": c_sec["quote"],
                    "version": kb["version"],
                    "score": round(max(item["score"] * 0.85, 1.0), 3),
                    "conflicts_with": list(c_sec.get("conflicts_with", [])),
                })

    return picked


@tool
def get_section(code: str) -> dict:
    """Tên: get_section — Đọc thông tin chuẩn hoá và dòng trích gốc của một mục tài liệu bài Lab theo mã K5-DayXX/FILE#mục.
    Input: code (str) — mã đoạn dạng 'K5-DayXX/FILE#mục' (ví dụ 'K5-Day14/CHECKPOINTS#lo-trinh-240p').
    Output: dict {"code", "lab", "file", "title", "summary", "quote", "version", "conflicts_with"} hoặc {} nếu không tồn tại.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu cục bộ)."""
    if not code or not isinstance(code, str):
        return {}
    kb = _load_kb()
    sec = kb["by_code"].get(code.strip().lower())
    if not sec:
        return {}
    return {
        "code": sec["code"],
        "lab": sec.get("lab", ""),
        "file": sec["file"],
        "title": sec["title"],
        "summary": sec["summary"],
        "quote": sec["quote"],
        "version": kb["version"],
        "conflicts_with": list(sec.get("conflicts_with", [])),
    }


@tool
def draft_coach_question(question: str, reason: str, cited_codes: str = "") -> str:
    """Tên: draft_coach_question — Soạn bản nháp câu hỏi ngắn gọn gửi Lab Coach khi tài liệu lab không ghi rõ hoặc 2 file lệch nhau.
    Input: question (str) — câu hỏi gốc; reason (str) — lý do cần xác nhận; cited_codes (str) — các mục tài liệu lab đã tra.
    Output: chuỗi văn bản bản nháp để học viên tự kiểm và tự gửi.
    Tác động ra ngoài: Không tự gửi tin (chỉ tạo bản nháp chờ học viên duyệt và tự gửi)."""
    q_clean = " ".join((question or "").strip().split())
    if len(q_clean) > 160:
        q_clean = q_clean[:157] + "..."
    checked = f" (em đã tra mục {cited_codes})" if cited_codes else " (em đã kiểm tra các file hướng dẫn của bài lab)"
    return (
        f"[Bản nháp hỏi Lab Coach — học viên tự kiểm và tự gửi]\n"
        f"\"Chào anh/chị Lab Coach, ở ca học của lớp mình em đang vướng câu hỏi: '{q_clean}'{checked}. "
        f"Do {reason}, nhờ anh/chị xác nhận giúp em quy định chính xác của bài lab này ạ. Em cảm ơn!\""
    )
