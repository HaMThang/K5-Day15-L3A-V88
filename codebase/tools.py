"""4 công cụ chỉ đọc (Read-Only) cho trợ lý bài Lab L3 — Nhóm V88."""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import tarfile
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
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
_ALLOWED_EXTS = {".md", ".py", ".yaml", ".yml", ".toml", ".txt", ".csv", ".json"}
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
            "summary": "\n".join(x.strip() for x in buf if x.strip())[:1500],  # đủ dài để giữ trọn bảng/danh sách của mục
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
    total_bytes = 0
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
            if os.path.islink(full_path) or not os.path.realpath(full_path).startswith(os.path.realpath(abs_root) + os.sep):
                continue  # không theo symlink ra ngoài thư mục bài lab
            try:
                size = os.path.getsize(full_path)
                is_data = ext in (".csv", ".json")
                if (size > _MAX_FILE_BYTES and not is_data) or total_bytes + min(size, _MAX_FILE_BYTES) > _MAX_TOTAL_BYTES:
                    continue
                with open(full_path, encoding="utf-8", errors="replace") as f:
                    lines = f.read(_MAX_FILE_BYTES).splitlines()
            except OSError:
                continue
            if is_data:
                lines = lines[:_DATA_PREVIEW_LINES]
            total_bytes += min(size, _MAX_FILE_BYTES)

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



# --- Nguồn bài lab do học viên đưa vào: thư mục trên máy hoặc link GitHub công khai ---------------
_GITHUB_URL_RE = re.compile(
    r"^https://github\.com/(?P<owner>[A-Za-z0-9][A-Za-z0-9-]{0,38})/(?P<repo>[A-Za-z0-9._-]{1,100}?)(?:\.git)?"
    r"(?:/tree/(?P<branch>[A-Za-z0-9._-]{1,100})(?P<path>(?:/[A-Za-z0-9._ -]{1,100}){0,12}))?/?$"
)
_GITHUB_HOSTS = {"codeload.github.com"}
_ALLOWED_GITHUB_OWNER = "VinUni-AI20k"  # chỉ nhận repo bài lab của khoá
_MAX_DOWNLOAD_BYTES = 40_000_000
_MAX_TOTAL_BYTES = 600_000
_DATA_PREVIEW_LINES = 20  # .csv/.json chỉ đọc phần đầu (tên cột, cấu trúc), không đọc hết dữ liệu có thể chứa thông tin cá nhân
_GITHUB_CACHE_DIR = os.path.join(tempfile.gettempdir(), "lab_compass_github")
_GITHUB_CACHE_SECONDS = 3600


class _GithubOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        if not newurl.startswith("https://") or urllib.parse.urlparse(newurl).hostname not in _GITHUB_HOSTS:
            raise urllib.error.HTTPError(newurl, 403, "redirect ra ngoài GitHub bị chặn", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_GithubOnlyRedirect)


def _allowed_roots() -> list[str]:
    raw = os.environ.get("LAB_ROOTS", "")
    roots = [r.strip() for r in raw.split(os.pathsep) if r.strip()] or [
        os.path.expanduser("~"),
        os.path.dirname(os.path.dirname(ROOT)),  # thư mục chứa repo nhóm và các bài lab đã clone
    ]
    return [os.path.normcase(os.path.realpath(r)) for r in roots]


def _resolve_folder(raw: str) -> tuple[str, str]:
    if ".." in re.split(r"[\\/]", raw):
        return "", "Đường dẫn không được chứa `..`. Bạn dán đường dẫn đầy đủ tới thư mục bài lab."
    if raw.startswith(("\\\\", "//")):
        return "", "Mình không đọc thư mục qua mạng nội bộ. Bạn chép bài lab về máy rồi dán đường dẫn."
    real = os.path.realpath(os.path.expanduser(raw))
    if not os.path.isdir(real):
        return "", "Không tìm thấy thư mục này trên máy. Bạn kiểm tra lại đường dẫn nhé."
    norm = os.path.normcase(real)
    if os.path.dirname(norm) == norm:
        return "", "Mình không quét cả ổ đĩa. Bạn chọn đúng thư mục của bài lab."
    if not any(norm == r or norm.startswith(r.rstrip("\\/") + os.sep) for r in _allowed_roots()):
        return "", "Thư mục này nằm ngoài vùng mình được phép đọc. Bạn để bài lab trong thư mục người dùng, hoặc thêm đường dẫn vào `LAB_ROOTS` trong `.env`."
    return real, ""


def _fetch_github(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    m = _GITHUB_URL_RE.match(url)
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.port or parsed.username or not m:
        return "", "Link phải là trang GitHub dạng `https://github.com/VinUni-AI20k/<repo>` hoặc `.../tree/<nhánh>/<thư mục>`. Mình không mở link ở trang khác."
    owner, repo, branch = m.group("owner"), m.group("repo"), m.group("branch")
    if owner.lower() != _ALLOWED_GITHUB_OWNER.lower():
        return "", "Mình chỉ nhận link bài lab trên GitHub của VinUni-AI20k (`https://github.com/VinUni-AI20k/...`)."
    sub = (m.group("path") or "").strip("/")
    if ".." in sub.split("/"):
        return "", "Link không được chứa `..`. Bạn dán đúng link thư mục bài lab trên GitHub."
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{repo}__{sub}__{branch or 'default'}").strip("-.")[:150]
    dest = os.path.join(_GITHUB_CACHE_DIR, slug)
    if os.path.isdir(dest) and time.time() - os.path.getmtime(dest) < _GITHUB_CACHE_SECONDS:
        return dest, ""
    # Tải bản nén của repo công khai qua codeload (không tốn lượt API, không gửi token),
    # đọc dạng luồng và chỉ giữ file chữ nằm trong thư mục được trỏ tới.
    branches = [branch] if branch else ["main", "master"]
    last_code = 0
    for br in branches:
        tar_url = f"https://codeload.github.com/{owner}/{repo}/tar.gz/{urllib.parse.quote(br)}"
        tmp = dest + ".part"
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        tmp_real = os.path.realpath(tmp)
        try:
            req = urllib.request.Request(tar_url, headers={"User-Agent": "lab-compass-readonly"})
            with _OPENER.open(req, timeout=20) as resp, tarfile.open(fileobj=_CappedReader(resp, _MAX_DOWNLOAD_BYTES), mode="r|gz") as tar:
                kept, total = 0, 0
                for member in tar:
                    if not member.isfile():
                        continue  # bỏ symlink, hardlink, thư mục, thiết bị
                    parts = member.name.split("/")[1:]  # bỏ thư mục gốc "<repo>-<nhánh>/"
                    rel = "/".join(parts)
                    if sub and not rel.startswith(sub + "/"):
                        continue
                    rel = rel[len(sub) + 1:] if sub else rel
                    ext = os.path.splitext(rel)[1].lower()
                    if (ext not in _ALLOWED_EXTS or _is_secret_filename(os.path.basename(rel))
                            or any(p in _SKIP_DIRS for p in rel.split("/"))
                            or (member.size > _MAX_FILE_BYTES and ext not in (".csv", ".json"))):
                        continue
                    target = os.path.realpath(os.path.join(tmp, *rel.split("/")))
                    if not target.startswith(tmp_real + os.sep):
                        continue  # tên file cố thoát khỏi thư mục tạm
                    data = tar.extractfile(member).read(_MAX_FILE_BYTES)
                    if ext in (".csv", ".json"):
                        data = b"\n".join(data.splitlines()[:_DATA_PREVIEW_LINES])
                    total += len(data)
                    if total > _MAX_TOTAL_BYTES or kept >= _MAX_SCAN_FILES:
                        break
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with open(target, "wb") as f:
                        f.write(data)
                    kept += 1
        except urllib.error.HTTPError as e:
            last_code = e.code
            shutil.rmtree(tmp, ignore_errors=True)
            if e.code == 404:
                continue
            if e.code in (403, 429):
                return "", "GitHub đang giới hạn lượt tải. Bạn thử lại sau ít phút, hoặc clone bài về máy rồi dán đường dẫn thư mục."
            return "", f"GitHub trả lỗi {e.code}, mình chưa tải được tài liệu."
        except ValueError:
            shutil.rmtree(tmp, ignore_errors=True)
            return "", "Repo trong link quá lớn để mình đọc nhanh. Bạn clone bài về máy rồi dán đường dẫn thư mục."
        except (urllib.error.URLError, TimeoutError, OSError, tarfile.TarError):
            shutil.rmtree(tmp, ignore_errors=True)
            return "", "Không kết nối hoặc không đọc được repo trên GitHub. Bạn kiểm tra mạng, hoặc clone bài về máy rồi dán đường dẫn thư mục."
        if not kept:
            shutil.rmtree(tmp, ignore_errors=True)
            return "", "Thư mục trong link này không có file tài liệu nào mình đọc được (.md, .txt, .py, .csv, .json, .yaml), hoặc sai tên thư mục."
        shutil.rmtree(dest, ignore_errors=True)
        os.replace(tmp, dest)
        _REPO_CACHE.pop(os.path.abspath(dest), None)
        return dest, ""
    return "", ("Không mở được repo này: repo private, không tồn tại, hoặc sai tên nhánh. Mình chỉ đọc repo công khai."
                if last_code in (0, 404) else f"GitHub trả lỗi {last_code}.")


class _CappedReader:
    """Bọc luồng tải về, báo lỗi khi vượt trần dung lượng để không tải cả repo khổng lồ."""

    def __init__(self, raw: Any, cap: int) -> None:
        self.raw, self.cap, self.seen = raw, cap, 0

    def read(self, n: int = -1) -> bytes:
        chunk = self.raw.read(n if n and n > 0 else 65536)
        self.seen += len(chunk)
        if self.seen > self.cap:
            raise ValueError("quá lớn")
        return chunk


def resolve_lab_source(source: str) -> tuple[str, str]:
    """Đổi thứ học viên dán vào (thư mục trên máy hoặc link GitHub công khai) thành thư mục cục bộ chỉ để đọc.
    Trả về (đường_dẫn, "") khi được, hoặc ("", lời báo lỗi tiếng Việt). Không ghi gì vào thư mục của học viên."""
    raw = (source or "").strip().strip('"').strip("'")
    if not raw:
        return "", ""
    if len(raw) > 400:
        return "", "Đường dẫn hoặc link quá dài."
    if re.match(r"^[a-z][a-z0-9+.-]*:(//|\\\\)", raw, re.IGNORECASE) or raw.lower().startswith(("github.com", "www.")):
        return _fetch_github(raw if "://" in raw else "https://" + raw)
    path, err = _resolve_folder(raw)
    if err:
        return "", err
    if not _index_local_repo(path).get("sections"):
        return "", "Thư mục này không có tài liệu nào mình đọc được (.md, .txt, .py, .csv, .json, .yaml)."
    return path, ""


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
    checked = f" (em đã xem {cited_codes})" if cited_codes else " (em đã kiểm tra các file hướng dẫn của bài lab)"
    return (
        f"[Bản nháp hỏi Lab Coach, bạn xem lại rồi tự gửi]\n"
        f"\"Chào anh/chị Lab Coach, em đang vướng câu hỏi: '{q_clean}'{checked}. "
        f"Vì {reason}, anh/chị xác nhận giúp em quy định của bài lab này với ạ. Em cảm ơn!\""
    )
