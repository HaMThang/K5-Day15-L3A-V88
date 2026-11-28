"""4 công cụ chỉ đọc (Read-Only) cho trợ lý bài Lab L3 — Nhóm V88."""
from __future__ import annotations

import json
import math
import os
import re
import unicodedata
from collections import Counter
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

_DAY_RE = re.compile(r"\b(?:day|lab|ngay)\s*[-_]?0?(\d{1,2})\b")
_TOKEN_RE = re.compile(r"[a-z0-9_#.\-/]+")
_HEADING_RE = re.compile(r"^#{1,3}\s+\S+")
_SYMBOL_RE = re.compile(r"^(def |async def |class )")

_CACHE: dict[str, Any] | None = None
_REPO_CACHE: dict[str, dict[str, Any]] = {}


def _strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _normalize_day_mentions(folded: str) -> str:
    extras = [f"day{int(m.group(1)):02d}" for m in _DAY_RE.finditer(folded) if 1 <= int(m.group(1)) <= 30]
    return f"{folded} {' '.join(extras)}" if extras else folded


def _day_of(text: str) -> str:
    """Số ngày Lab ("03") nhắc trong câu hỏi, tên thư mục hoặc mã mục; "" nếu không có."""
    m = _DAY_RE.search(_strip_accents((text or "").lower()))
    return f"{int(m.group(1)):02d}" if m and 1 <= int(m.group(1)) <= 30 else ""


def _tokenize(text: str) -> list[str]:
    folded = _normalize_day_mentions(_strip_accents(text.lower()))
    tokens: list[str] = []
    for raw in _TOKEN_RE.findall(folded):
        for tok in re.split(r"[/#]", raw):
            tok = tok.strip(".-_")
            if tok and not (tok in _STOPWORDS and len(tok) <= 4):
                tokens.append(tok)
    return tokens


def _is_secret_filename(name: str) -> bool:
    low = name.lower()
    if low == ".env" or (low.startswith(".env.") and low != ".env.example"):
        return True
    return low.endswith((".pem", ".key", ".pfx")) or "credentials" in low or "secret" in low


def _section_view(sec: dict[str, Any], version: str, score: float | None = None) -> dict[str, Any]:
    view: dict[str, Any] = {
        "code": sec["code"],
        "lab": sec.get("lab", ""),
        "file": sec.get("file", ""),
        "title": sec["title"],
        "summary": sec["summary"],
        "quote": sec["quote"],
        "version": version,
        "conflicts_with": list(sec.get("conflicts_with", [])),
    }
    if score is not None:
        view["score"] = round(score, 3)
    return view


def _load_kb() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    if not os.path.exists(INDEX_PATH):
        _CACHE = {"version": "unknown", "sections": [], "by_code": {}, "idf": {}, "avgdl": 1.0, "tf_maps": [], "doc_lens": []}
        return _CACHE

    with open(INDEX_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    sections: list[dict[str, Any]] = raw.get("sections", [])
    by_code = {s["code"].lower(): s for s in sections}
    tf_maps: list[Counter[str]] = []
    doc_lens: list[int] = []
    df: Counter[str] = Counter()

    for sec in sections:
        kws = " ".join(sec.get("keywords", []))
        weighted = " ".join([
            sec.get("code", ""),
            sec.get("lab", ""),
            sec.get("title", ""),
            sec.get("title", ""),
            kws,
            kws,
            sec.get("summary", ""),
            sec.get("quote", ""),
            sec.get("file", ""),
        ])
        toks = _tokenize(weighted)
        counts = Counter(toks)
        tf_maps.append(counts)
        doc_lens.append(len(toks))
        df.update(counts.keys())

    n_docs = max(len(sections), 1)
    avgdl = max(sum(doc_lens) / n_docs, 1.0)
    idf = {term: math.log(1.0 + (n_docs - freq + 0.5) / (freq + 0.5)) for term, freq in df.items()}

    _CACHE = {
        "version": raw.get("version", "K5-L3-Phase1-Labs"),
        "sections": sections,
        "by_code": by_code,
        "tf_maps": tf_maps,
        "doc_lens": doc_lens,
        "idf": idf,
        "avgdl": avgdl,
    }
    return _CACHE


def _chunk_markdown(repo_name: str, rel_path: str, fname: str, lines: list[str]) -> tuple[str, list[dict[str, Any]]]:
    chunks: list[tuple[str, int, list[str]]] = []
    cur_title, cur_start, cur_buf = fname, 1, []
    for idx, ln in enumerate(lines, start=1):
        if _HEADING_RE.match(ln):
            if cur_buf:
                chunks.append((cur_title, cur_start, cur_buf))
            cur_title, cur_start, cur_buf = ln.lstrip("#").strip()[:90], idx, [ln]
        else:
            cur_buf.append(ln)
    if cur_buf:
        chunks.append((cur_title, cur_start, cur_buf))

    outline_entry = f"{rel_path}: " + " | ".join(t for t, _, _ in chunks[:6])
    secs: list[dict[str, Any]] = []
    for c_idx, (title, start_ln, buf) in enumerate(chunks[:12], start=1):
        end_ln = start_ln + len(buf) - 1
        slug = re.sub(r"[^a-z0-9]+", "-", _strip_accents(title.lower())).strip("-")[:28] or f"sec{c_idx}"
        body_txt = " ".join(x.strip() for x in buf if x.strip())
        secs.append({
            "code": f"{repo_name}/{rel_path}#{slug}",
            "lab": repo_name,
            "file": f"{rel_path}:{start_ln}-{end_ln}",
            "title": f"{rel_path} · {title}",
            "keywords": [],
            "summary": body_txt[:420],
            "quote": body_txt[:220],
            "conflicts_with": [],
        })
    return outline_entry, secs


def _chunk_code(repo_name: str, rel_path: str, lines: list[str]) -> tuple[str, list[dict[str, Any]]]:
    sigs: list[str] = []
    todos: list[str] = []
    for idx, ln in enumerate(lines, start=1):
        stripped = ln.strip()
        if _SYMBOL_RE.match(stripped):
            sigs.append(f"{stripped.split(':')[0]} (L{idx})")
        if "TODO" in ln or "FIXME" in ln or "NotImplementedError" in ln:
            todos.append(f"L{idx}: {stripped[:70]}")

    meta = ", ".join(sigs[:6]) if sigs else f"{len(lines)} dòng"
    if todos:
        meta += " · TODO: " + "; ".join(todos[:3])

    secs: list[dict[str, Any]] = []
    step = 60
    for start_idx in range(0, min(len(lines), 240), step):
        chunk = lines[start_idx:start_idx + step]
        s_ln, e_ln = start_idx + 1, start_idx + len(chunk)
        snippet = "\n".join(f"L{s_ln + i}: {line}" for i, line in enumerate(chunk[:18]))
        secs.append({
            "code": f"{repo_name}/{rel_path}#L{s_ln}-L{e_ln}",
            "lab": repo_name,
            "file": f"{rel_path}:{s_ln}-{e_ln}",
            "title": f"{rel_path} (dòng {s_ln}–{e_ln})",
            "keywords": [],
            "summary": " ".join(x.strip() for x in chunk if x.strip())[:420],
            "quote": snippet[:260],
            "conflicts_with": [],
        })
    return f"{rel_path}: {meta}", secs


def _index_local_repo(repo_path: str) -> dict[str, Any]:
    abs_root = os.path.abspath(repo_path)
    if abs_root in _REPO_CACHE:
        return _REPO_CACHE[abs_root]
    if not os.path.isdir(abs_root):
        return {"exists": False, "repo_name": "", "files_md": [], "files_code": [], "outline": [], "sections": [], "tf_maps": [], "doc_lens": [], "by_code": {}}

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
                out_item, new_secs = _chunk_markdown(repo_name, rel_path, fname, lines)
            else:
                files_code.append(rel_path)
                out_item, new_secs = _chunk_code(repo_name, rel_path, lines)
            outline.append(out_item)
            sections.extend(new_secs)

    tf_maps: list[Counter[str]] = []
    doc_lens: list[int] = []
    for s in sections:
        toks = _tokenize(" ".join([s["code"], s["title"], s["summary"], s["quote"], s["file"]]))
        tf_maps.append(Counter(toks))
        doc_lens.append(len(toks))

    info = {
        "exists": True,
        "repo_name": repo_name,
        "files_md": files_md,
        "files_code": files_code,
        "outline": outline[:25],
        "sections": sections,
        "tf_maps": tf_maps,
        "doc_lens": doc_lens,
        "by_code": {s["code"].lower(): s for s in sections},
    }
    _REPO_CACHE[abs_root] = info
    return info


@tool
def scan_lab_codebase(repo_path: str = "", lab_hint: str = "") -> dict:
    """Tên: scan_lab_codebase — Đọc cấu trúc thư mục bài Lab đã clone hoặc chỉ mục bài Lab K5.
    Input: repo_path (str, tuỳ chọn) — đường dẫn thư mục bài lab; lab_hint (str) — câu hỏi/tên bài lab.
    Output: dict {"mode_source", "lab_name", "files_md", "files_code", "outline"}.
    Tác động ra ngoài: Không (chỉ đọc file cục bộ, bỏ qua .env/.git)."""
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
    prefix = f"k5-day{day_matches[0]}" if day_matches else ""

    matched = [s for s in kb["sections"] if not prefix or s["code"].lower().startswith(prefix)] or kb["sections"][:8]
    files_seen = sorted({s.get("file", "").split(":")[0] for s in matched if s.get("file")})
    outline = [f"[{s['code']}] ({s.get('file', '')}): {s['title']}" for s in matched[:10]]
    lab_label = matched[0].get("lab", kb["version"]) if prefix and matched else kb["version"]
    return {
        "mode_source": "kb_index_snapshot",
        "lab_name": lab_label,
        "files_md": files_seen,
        "files_code": [],
        "outline": outline,
    }


@tool
def search_docs(query: str, k: int = 5, repo_path: str = "") -> list:
    """Tên: search_docs — Tra cứu BM25 trên tài liệu/mã khung bài Lab và chỉ mục K5 (kèm mục đối chiếu).
    Input: query (str) — câu hỏi hoặc lỗi của học viên; k (int, mặc định 5); repo_path (str, tuỳ chọn).
    Output: danh sách dict {"code", "lab", "file", "title", "summary", "quote", "version", "score", "conflicts_with"}.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu cục bộ)."""
    if not query or not query.strip():
        return []
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    kb = _load_kb()
    sections = list(kb["sections"])
    tf_maps = list(kb["tf_maps"])
    doc_lens = list(kb["doc_lens"])
    by_code = dict(kb["by_code"])

    # Chỉ giữ mục chỉ mục của đúng ngày Lab đang hỏi (+ quy ước chung), tránh trích nhầm bài ngày khác.
    want_day = _day_of(query)
    local = _index_local_repo(repo_path.strip()) if repo_path and repo_path.strip() else {}
    if local.get("exists"):
        want_day = want_day or _day_of(local["repo_name"])
    if want_day or local.get("exists"):
        keep = [i for i, sec in enumerate(sections) if _day_of(sec["code"]) in ("", want_day)]
        sections = [sections[i] for i in keep]
        tf_maps = [tf_maps[i] for i in keep]
        doc_lens = [doc_lens[i] for i in keep]

    if local.get("exists") and local["sections"]:
        sections.extend(local["sections"])
        tf_maps.extend(local["tf_maps"])
        doc_lens.extend(local["doc_lens"])
        by_code.update(local["by_code"])

    if not sections:
        return []

    q_folded = _normalize_day_mentions(_strip_accents(query.lower()))
    idf = kb["idf"]
    avgdl = max(sum(doc_lens) / len(doc_lens), 1.0)
    k1, b = 1.5, 0.75

    scored: list[tuple[float, dict[str, Any]]] = []
    for sec, tf_map, dl in zip(sections, tf_maps, doc_lens):
        if not dl:
            continue
        score = 0.0
        for qt in q_tokens:
            tf = tf_map.get(qt, 0)
            if tf:
                score += idf.get(qt, 1.2) * (tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * dl / avgdl))

        for kw in sec.get("keywords", []):
            kw_f = _strip_accents(kw.lower()).strip()
            if len(kw_f) >= 3 and kw_f in q_folded:
                score += 2.2

        if score > 0.0:
            scored.append((score, sec))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_k = max(1, min(int(k), 8))
    picked: list[dict[str, Any]] = []
    seen: set[str] = set()

    for score, sec in scored[:top_k]:
        seen.add(sec["code"].lower())
        picked.append(_section_view(sec, kb["version"], score=score))

    for item in list(picked[:2]):
        for conflict_code in item.get("conflicts_with", []):
            c_key = conflict_code.lower()
            if c_key not in seen and c_key in by_code:
                seen.add(c_key)
                picked.append(_section_view(by_code[c_key], kb["version"], score=max(item["score"] * 0.85, 1.0)))

    return picked


@tool
def get_section(code: str, repo_path: str = "") -> dict:
    """Tên: get_section — Lấy trích đoạn và dòng gốc (file:dòng) theo mã mục.
    Input: code (str) — mã đoạn dạng 'K5-DayXX/FILE#mục'; repo_path (str, tuỳ chọn).
    Output: dict thông tin mục hoặc {} nếu không tìm thấy.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu cục bộ)."""
    if not code or not isinstance(code, str):
        return {}
    key = code.strip().lower()
    if repo_path and repo_path.strip():
        local = _index_local_repo(repo_path.strip())
        if key in local.get("by_code", {}):
            return _section_view(local["by_code"][key], "local_cloned_repo")
    kb = _load_kb()
    sec = kb["by_code"].get(key)
    return _section_view(sec, kb["version"]) if sec else {}


@tool
def draft_coach_question(question: str, reason: str, cited_codes: str = "") -> str:
    """Tên: draft_coach_question — Soạn nháp câu hỏi gửi Lab Coach khi thiếu nguồn hoặc hai file lệch nhau.
    Input: question (str) — câu hỏi gốc; reason (str) — lý do cần xác nhận; cited_codes (str) — mã mục đã tra.
    Output: chuỗi văn bản bản nháp để học viên tự kiểm và gửi.
    Tác động ra ngoài: Không tự gửi tin (chỉ tạo bản nháp chờ người dùng duyệt)."""
    q_clean = " ".join((question or "").strip().split()).rstrip(" .")
    if len(q_clean) > 160:
        q_clean = q_clean[:157] + "..."
    reason = re.sub(r"[;,]\s*(cần|nhờ)\s.*(xác nhận|hỏi).*$", "", (reason or "").strip(), flags=re.IGNORECASE)
    reason = reason.strip().rstrip(".;:, ")
    if reason[1:2].islower():  # "Tài liệu..." -> "tài liệu..." sau chữ "Vì"; giữ nguyên "CHECKPOINTS.md..."
        reason = reason[0].lower() + reason[1:]
    checked = f" (em đã tra mục {cited_codes})" if cited_codes else " (em đã kiểm tra các file hướng dẫn của bài lab)"
    return (
        f"[Bản nháp hỏi Lab Coach, bạn xem lại rồi tự gửi]\n"
        f"\"Chào anh/chị Lab Coach, em đang vướng câu hỏi: '{q_clean}'{checked}. "
        f"Vì {reason}, anh/chị xác nhận giúp em quy định của bài lab này với ạ. Em cảm ơn!\""
    )
