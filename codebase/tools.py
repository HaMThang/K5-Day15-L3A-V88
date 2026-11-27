"""Công cụ của bài toán — Nhóm V88 (Track A · Trợ lý hướng dẫn làm bài Lab L3 theo 3 mức sư phạm).

Mỗi công cụ là một hàm Python có @tool, 100% Read-Only (không sửa file, không cài môi trường, không chạy lệnh).
Docstring ghi đúng 4 ý khớp sơ đồ ở spec.md §4: tên · input · output · có tác động ra ngoài không.
Chỉ dùng thư viện chuẩn của Python 3.10+.
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

_SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache",
    ".mypy_cache", "data-btc", ".idea", ".vscode", ".claude", ".gemini", ".codex",
}
_ALLOWED_EXTS = {".md", ".py", ".yaml", ".yml", ".toml", ".txt"}
_MAX_SCAN_FILES = 60
_MAX_FILE_BYTES = 48_000

_CACHE: dict[str, Any] | None = None
_REPO_CACHE: dict[str, dict[str, Any]] = {}


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


def _is_secret_filename(name: str) -> bool:
    low = name.lower()
    if low == ".env" or low.startswith(".env.") and low != ".env.example":
        return True
    return low.endswith((".pem", ".key", ".pfx")) or "credentials" in low or "secret" in low


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


def _index_local_repo(repo_path: str) -> dict[str, Any]:
    """Đọc tĩnh (Read-Only) toàn bộ file .md/.py/.yaml hợp lệ trong thư mục bài lab học viên vừa clone."""
    abs_root = os.path.abspath(repo_path)
    if abs_root in _REPO_CACHE:
        return _REPO_CACHE[abs_root]
    if not os.path.isdir(abs_root):
        return {"exists": False, "repo_name": "", "files_md": [], "files_code": [], "outline": [], "sections": [], "by_code": {}}

    repo_name = os.path.basename(abs_root.rstrip("\\/")) or "LocalLab"
    files_md: list[str] = []
    files_code: list[str] = []
    outline: list[str] = []
    sections: list[dict[str, Any]] = []

    count = 0
    for cur_root, dirs, files in os.walk(abs_root):
        dirs[:] = sorted(d for d in dirs if d not in _SKIP_DIRS and not d.startswith("."))
        for fname in sorted(files):
            if count >= _MAX_SCAN_FILES:
                break
            if _is_secret_filename(fname):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in _ALLOWED_EXTS:
                continue
            full_path = os.path.join(cur_root, fname)
            try:
                if os.path.getsize(full_path) > _MAX_FILE_BYTES:
                    continue
                with open(full_path, encoding="utf-8", errors="replace") as f:
                    lines = f.read().splitlines()
            except OSError:
                continue

            count += 1
            rel_path = os.path.relpath(full_path, abs_root).replace(os.sep, "/")
            if ext == ".md":
                files_md.append(rel_path)
            else:
                files_code.append(rel_path)

            # Tách đoạn theo tiêu đề Markdown hoặc hàm/lớp Python để định vị file:dòng chính xác
            if ext == ".md":
                chunks: list[tuple[str, int, list[str]]] = []
                cur_title, cur_start, cur_buf = fname, 1, []
                for idx, ln in enumerate(lines, start=1):
                    if re.match(r"^#{1,3}\s+\S+", ln):
                        if cur_buf:
                            chunks.append((cur_title, cur_start, cur_buf))
                        cur_title = ln.lstrip("#").strip()[:90]
                        cur_start = idx
                        cur_buf = [ln]
                    else:
                        cur_buf.append(ln)
                if cur_buf:
                    chunks.append((cur_title, cur_start, cur_buf))

                headings = [t for t, _, _ in chunks[:6]]
                outline.append(f"{rel_path}: " + " | ".join(headings))
                for c_idx, (title, start_ln, buf) in enumerate(chunks[:12], start=1):
                    end_ln = start_ln + len(buf) - 1
                    slug = re.sub(r"[^a-z0-9]+", "-", _strip_accents(title.lower())).strip("-")[:28] or f"sec{c_idx}"
                    code_id = f"{repo_name}/{rel_path}#{slug}"
                    body_txt = " ".join(x.strip() for x in buf if x.strip())
                    sections.append({
                        "code": code_id,
                        "lab": repo_name,
                        "file": f"{rel_path}:{start_ln}-{end_ln}",
                        "title": f"{rel_path} · {title}",
                        "keywords": [],
                        "summary": body_txt[:420],
                        "quote": body_txt[:220],
                        "conflicts_with": [],
                    })
            else:
                sigs: list[str] = []
                todos: list[str] = []
                for idx, ln in enumerate(lines, start=1):
                    stripped = ln.strip()
                    if re.match(r"^(def |async def |class )", stripped):
                        sigs.append(f"{stripped.split(':')[0]} (L{idx})")
                    if "TODO" in ln or "FIXME" in ln or "NotImplementedError" in ln:
                        todos.append(f"L{idx}: {stripped[:70]}")
                meta = ", ".join(sigs[:6]) if sigs else f"{len(lines)} dòng"
                if todos:
                    meta += " · TODO: " + "; ".join(todos[:3])
                outline.append(f"{rel_path}: {meta}")

                step = 60
                for start_idx in range(0, min(len(lines), 240), step):
                    chunk_lines = lines[start_idx:start_idx + step]
                    s_ln = start_idx + 1
                    e_ln = start_idx + len(chunk_lines)
                    code_id = f"{repo_name}/{rel_path}#L{s_ln}-L{e_ln}"
                    snippet = "\n".join(f"L{s_ln + i}: {l}" for i, l in enumerate(chunk_lines[:18]))
                    sections.append({
                        "code": code_id,
                        "lab": repo_name,
                        "file": f"{rel_path}:{s_ln}-{e_ln}",
                        "title": f"{rel_path} (dòng {s_ln}–{e_ln})",
                        "keywords": [],
                        "summary": " ".join(x.strip() for x in chunk_lines if x.strip())[:420],
                        "quote": snippet[:260],
                        "conflicts_with": [],
                    })

    by_code = {s["code"].lower(): s for s in sections}
    info = {
        "exists": True,
        "repo_name": repo_name,
        "files_md": files_md,
        "files_code": files_code,
        "outline": outline[:25],
        "sections": sections,
        "by_code": by_code,
    }
    _REPO_CACHE[abs_root] = info
    return info


@tool
def scan_lab_codebase(repo_path: str = "", lab_hint: str = "") -> dict:
    """Tên: scan_lab_codebase — Đọc tĩnh toàn bộ cấu trúc codebase bài Lab học viên vừa fork/clone (hoặc bản đồ bài Lab từ chỉ mục K5).
    Input: repo_path (str, tuỳ chọn) — đường dẫn thư mục bài lab cục bộ; lab_hint (str) — câu hỏi/tên bài lab để lọc nhanh.
    Output: dict {"mode_source", "lab_name", "files_md", "files_code", "outline"} tóm tắt cây thư mục, các mục hướng dẫn và hàm/TODO.
    Tác động ra ngoài: Không (100% Read-Only cục bộ, tự lọc bỏ .env/.git, tuyệt đối không chạy code hay sửa file)."""
    if repo_path and repo_path.strip():
        local = _index_local_repo(repo_path.strip())
        if local.get("exists"):
            return {
                "mode_source": "local_cloned_repo",
                "lab_name": local["repo_name"],
                "files_md": local["files_md"],
                "files_code": local["files_code"],
                "outline": local["outline"],
            }

    kb = _load_kb()
    folded_hint = _normalize_day_mentions(_strip_accents((lab_hint or "").lower()))
    day_matches = re.findall(r"\bday(\d{2})\b", folded_hint)
    target_prefix = f"k5-day{day_matches[0]}" if day_matches else ""

    matched_secs = [
        s for s in kb["sections"]
        if (not target_prefix) or s["code"].lower().startswith(target_prefix)
    ]
    if not matched_secs:
        matched_secs = kb["sections"][:8]

    files_seen = sorted({s.get("file", "").split(":")[0] for s in matched_secs if s.get("file")})
    outline = [f"[{s['code']}] ({s.get('file', '')}): {s['title']}" for s in matched_secs[:10]]
    lab_label = matched_secs[0].get("lab", kb["version"]) if target_prefix and matched_secs else kb["version"]
    return {
        "mode_source": "kb_index_snapshot",
        "lab_name": lab_label,
        "files_md": files_seen,
        "files_code": [],
        "outline": outline,
    }


@tool
def search_docs(query: str, k: int = 5, repo_path: str = "") -> list:
    """Tên: search_docs — Tra cứu BM25 trên các file hướng dẫn/mã khung của codebase bài Lab đang mở và chỉ mục chuẩn K5 (tự kéo mục mâu thuẫn).
    Input: query (str) — câu hỏi hoặc log lỗi của học viên; k (int, mặc định 5); repo_path (str, tuỳ chọn) — thư mục bài lab đã clone.
    Output: danh sách dict {"code", "lab", "file", "title", "summary", "quote", "version", "score", "conflicts_with"}.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu cục bộ, không thực thi lệnh)."""
    kb = _load_kb()
    all_sections = list(kb["sections"])
    all_doc_tokens = list(kb["doc_tokens"])
    by_code = dict(kb["by_code"])

    if repo_path and repo_path.strip():
        local = _index_local_repo(repo_path.strip())
        if local.get("exists") and local["sections"]:
            for s in local["sections"]:
                all_sections.append(s)
                all_doc_tokens.append(_tokenize(" ".join([s["code"], s["title"], s["summary"], s["quote"], s["file"]])))
                by_code[s["code"].lower()] = s

    if not all_sections or not query or not query.strip():
        return []

    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    q_folded = _normalize_day_mentions(_strip_accents(query.lower()))
    idf = kb["idf"]
    avgdl = max(sum(len(t) for t in all_doc_tokens) / max(len(all_doc_tokens), 1), 1.0)
    k1, b = 1.5, 0.75

    scored: list[tuple[float, dict[str, Any]]] = []
    for sec, d_toks in zip(all_sections, all_doc_tokens):
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
            term_idf = idf.get(qt, 1.2)
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
            if c_key not in seen_codes and c_key in by_code:
                c_sec = by_code[c_key]
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
def get_section(code: str, repo_path: str = "") -> dict:
    """Tên: get_section — Đọc trích đoạn kèm số dòng gốc (file:dòng) của một mục tài liệu hoặc file code khung bài Lab.
    Input: code (str) — mã đoạn dạng 'K5-DayXX/FILE#mục' hoặc mã đoạn trong repo vừa clone; repo_path (str, tuỳ chọn).
    Output: dict {"code", "lab", "file", "title", "summary", "quote", "version", "conflicts_with"} hoặc {} nếu không tồn tại.
    Tác động ra ngoài: Không (100% Read-Only cục bộ)."""
    if not code or not isinstance(code, str):
        return {}
    key = code.strip().lower()
    if repo_path and repo_path.strip():
        local = _index_local_repo(repo_path.strip())
        if key in local.get("by_code", {}):
            sec = local["by_code"][key]
            return {
                "code": sec["code"],
                "lab": sec.get("lab", ""),
                "file": sec["file"],
                "title": sec["title"],
                "summary": sec["summary"],
                "quote": sec["quote"],
                "version": "local_cloned_repo",
                "conflicts_with": [],
            }
    kb = _load_kb()
    sec = kb["by_code"].get(key)
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
