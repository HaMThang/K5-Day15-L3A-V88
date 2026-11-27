# Team V88 · agent setup prompt (v2, dùng cho mọi coding agent)

> **Dành cho Hoàng, Cương, Thắng (và Hưng khi đổi máy).** Dùng được với Claude Code, Codex CLI, Cursor, Gemini CLI, GitHub Copilot (agent mode)… Repo đã cấu hình sẵn, không ai phải tạo file nữa. Prompt chỉ **kiểm tra (read-only)** máy của bạn và nạp bối cảnh.
>
> **Luật chung nằm ở một chỗ duy nhất: `AGENTS.md`.** `CLAUDE.md` và `GEMINI.md` chỉ là file trỏ về `AGENTS.md`. Muốn đổi luật thì sửa `AGENTS.md` qua PR.
>
> | Agent | Tự đọc file nào | Cần làm thêm |
> |---|---|---|
> | Codex CLI, Cursor, Copilot (VS Code), Jules, Aider… | `AGENTS.md` | không |
> | Claude Code | `CLAUDE.md` → `@AGENTS.md` | không (đã có `.claude/settings.json`) |
> | Gemini CLI | `GEMINI.md` → `@AGENTS.md` | không |
> | Agent khác | — | dán prompt dưới đây, bước 1 bắt nó đọc `AGENTS.md` |
>
> **Các bước (PowerShell, Windows):**
> 1. Lần đầu: `git clone https://github.com/HaMThang/K5-Day15-L3A-V88.git` rồi `cd K5-Day15-L3A-V88`. Đã clone rồi: `git checkout main` rồi `git pull origin main`.
> 2. `copy .env.example .env`, mở `.env` điền `MODEL_PROVIDER`, `MODEL_NAME`, `API_KEY` của nhóm (hỏi Hoàng). Không gửi key qua kênh công khai, không commit `.env`.
> 3. Mở agent ở thư mục repo, dán đoạn từ `---BEGIN PROMPT---` đến `---END PROMPT---`.
> 4. Agent báo `PASS` hết là xong. Có `FAIL` thì gửi bảng báo cáo vào nhóm.
> 5. Làm việc trên nhánh riêng: `git checkout -b feat/<ten>-<viec>`, commit nhỏ, push nhánh, mở PR vào `main`. Không push thẳng `main` (trừ Hưng khi nộp checkpoint).

---BEGIN PROMPT---

# Task: verify my machine for team V88's hackathon repo (READ-ONLY)

You are a coding agent onboarding me to an existing, already-configured repo. Do not create, edit, delete, commit or push anything. Do not install packages. Never open or print `.env` (only check that it exists). Report each check as `PASS`, `FAIL` or `CHƯA KIỂM` with the exact command you ran. Reply in Vietnamese.

## 1. Load context first
Read, in this order: `AGENTS.md` (the binding rules for all agents, including the `<!-- team-harness v1 -->` section), `docs/checkpoints-context.md`, `spec.md` §4 and §7, `TEAMS.md`. If your tool also loaded `CLAUDE.md` or `GEMINI.md`, treat them as pointers to `AGENTS.md`; if they ever disagree, `AGENTS.md` wins. Use these files for the checks and for step 4; do not summarise them in full.

## 2. Environment checks
1. OS and shell. Use matching syntax: Windows PowerShell → `python` (or `py`), `Test-Path`; macOS/Linux → `python3`, `test -f`.
2. `git rev-parse --show-toplevel` → ends with `K5-Day15-L3A-V88`; `run.py`, `spec.md`, `eval/`, `codebase/`, `data/kb_index.json` exist at that root.
3. `python --version` → ≥ 3.10.
4. `git branch --show-current` and `git status --short` → report branch and uncommitted files. Warn if on `main` with local changes.
5. `git fetch origin` then `git status -sb` → report if behind `origin/main`.
6. `.env` exists (existence only). Missing → FAIL, tell me to run `copy .env.example .env` (Windows) or `cp .env.example .env`.
7. `git check-ignore -v .env data-btc/` → both ignored.
8. `AGENTS.md` contains the line `<!-- team-harness v1 -->` exactly once.
9. Pointer files, only report: `CLAUDE.md` and `GEMINI.md` exist and reference `AGENTS.md`.
10. Tool-specific, optional:
    - Claude Code: `.claude/settings.json` deny list contains `Read(./.env)` and `Bash(git push:*)`.
    - Other agents: say which rule mechanism you have (sandbox / approval mode / ignore file) and confirm you will not read `.env` or run `git push` without my explicit OK. Do not create config files.

## 3. Repo checks (no model call, nothing committed)
1. `python run.py check` → copy the "Cần xem lại" warnings verbatim.
2. `python run.py eval --fake` → must finish all cases (writes `eval/run-fake.csv`, git-ignored).
3. Optional, only if I say yes: `python run.py eval --try 1` → report tokens in/out > 0 (one real model call).

## 4. Brief me (max 10 lines)
- Current checkpoint and time left (from `docs/checkpoints-context.md`, UTC+7).
- My role and owned files (match `git config user.name` to `TEAMS.md`; if unclear, ask which member I am).
- The 3 rules I must never break (from `AGENTS.md` §1).
- Next concrete step for my role.

## 5. Report format
A table `check | command | PASS/FAIL/CHƯA KIỂM | note`, then the brief, then "Việc cần làm tay". Nothing else.

---END PROMPT---

## Ghi chú cho lead
- v1 (BOOTSTRAP) đã chạy trên máy Hưng; mọi file cấu hình đã nằm trong repo nên v2 chỉ còn kiểm tra.
- `AGENTS.md` mục 7 (mới) gom phần "quick facts + decisions" trước đây nằm trong `CLAUDE.md`, để agent nào cũng đọc được.
- Thêm agent mới (vd Windsurf, Kiro) chỉ cần một file trỏ 3 dòng giống `GEMINI.md`, không chép luật.
