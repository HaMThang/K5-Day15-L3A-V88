# AGENTS.md — hướng dẫn cho coding agent (Claude Code, Cursor, Codex…) làm việc trong repo này

> Ôn lại: ngày 12 · lab ngày 12. Nhóm sửa file này cho khớp bài của mình (thêm quy ước riêng, bỏ dòng không dùng).

## Repo này là gì

Repo nộp bài hackathon AI20K của nhóm: một bản chạy thử AI cho **một lát cắt** (xem `spec.md` §4), kèm bằng chứng, bộ câu thử và mô phỏng chi phí. Mọi câu trả lời phải chạy được bằng các lệnh dưới đây.

## Lệnh

```
python run.py                    # chạy bản chạy thử
python run.py check              # kiểm eval/benchmark.csv + eval/metric_spec.yaml
python run.py eval --try         # thử 3 câu đầu
python run.py eval               # chạy cả bộ → eval/run-N.csv + traces/run-N.jsonl
python run.py score eval/run-N.csv
python run.py simulate --try     # thử mô phỏng chi phí 10 phiên
python run.py simulate           # mô phỏng chi phí → cost/simulate-N.csv
```

Khung chỉ dùng thư viện chuẩn của Python. Thêm thư viện thì ghi vào `requirements.txt`.

## Cấu trúc code

| File | Ai sửa | Hợp đồng |
|---|---|---|
| `codebase/agent.py` | nhóm | `answer(text) -> {"output": str}` — luồng chính, đúng hình dạng ở `spec.md` §4 |
| `codebase/ai.py` | nhóm | `call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`, giữ `@model_call`. Token lấy từ `usage` của API, không ước lượng |
| `codebase/tools.py` | nhóm | mỗi công cụ một hàm có `@tool`, docstring: tên · input · output · có tác động ra ngoài không |
| `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py` | **khung — không sửa** | ghi trace, chạy bộ câu thử, mô phỏng chi phí |

## Luật — agent KHÔNG được làm

- Không commit `.env`, API key, dữ liệu cá nhân thật, nguyên file data BTC cấp.
- Không sửa `eval/run-*.csv`, `cost/simulate-*.csv`, `traces/*` đã chạy (trừ điền cột `pass`, `ghi_chu`).
- Không sửa chuẩn "đạt" (`spec.md` §7), `eval/metric_spec.yaml` sau CP2; không xoá câu thử trượt, không sửa `expected` cho khớp output.
- Không bịa người được phỏng vấn, trích dẫn, câu trả lời khảo sát, số liệu. Số không có nguồn thì ghi rõ *(tự ước tính)*.
- Công cụ có tác động ra ngoài (gửi tin, sửa dữ liệu, chấm điểm): chỉ tạo bản nháp chờ người duyệt.
- Không viết prompt "giấu" câu thử vào code (vd so khớp nguyên văn input của bộ câu thử).

## Quy ước của nhóm

- Ngôn ngữ trả lời người dùng: Tiếng Việt (giữ nguyên tên file và thuật ngữ kỹ thuật)
- Phong cách code / đặt tên: PEP 8, snake_case, type hints cho hàm mới, chỉ dùng thư viện chuẩn Python 3.10+
- Ai duyệt thay đổi do agent tạo trước khi commit: 1 thành viên khác duyệt PR; Hưng (Đội trưởng) duyệt thay đổi ở `spec.md` và `eval/`
- Bối cảnh hackathon, mốc nộp, luật phạt: đọc `docs/checkpoints-context.md` trước khi làm việc.

<!-- team-harness v1 -->
## Team V88 harness rules (binding for every agent)

### 1. Hackathon hard rules (breaking one = lost points)
- Real AI call in the demo and in `eval` runs; `fake` mode is only for checking the pipeline.
- Never commit `.env`, API keys, real personal data, or raw organiser data (`data-btc/`).
- `spec.md` §7 pass threshold and `eval/metric_spec.yaml` are LOCKED after CP2 (Fri 27/11 19:30, UTC+7). Never edit them after that, even if asked casually; ask Henry explicitly.
- Never delete or rewrite failing eval cases; never change `expected` to match output; never hard-code benchmark inputs in prompts or code.
- Never edit finished runs (`eval/run-N.csv`, `cost/simulate-N.csv`, `traces/run-N.jsonl`) except the `pass` / `ghi_chu` columns. These numbered runs MUST be committed.
- Never invent interviewees, quotes, survey answers or numbers. Unsourced numbers are marked *(tự ước tính)*.

### 2. Truth and evidence
- Source of truth: `spec.md` (design, §4 architecture, §7 threshold), `eval/metric_spec.yaml` (metrics), `evidence/` (user evidence), `TEAMS.md`, `canvas.md`.
- Code wins: when code and docs disagree, report both `file:line` and add the item to `spec.md` §10 changelog as an open question. Do not silently edit docs to match code.
- Every "pass / works / verified" claim cites the exact command and the produced file (e.g. `python run.py eval` → `eval/run-2.csv`). Otherwise write `CHƯA KIỂM`.
- LLM results are non-deterministic: report `k/n` (e.g. 18/25 pass), not "it works". If an LLM judges `pass`, it must be a different call from the generator, `temperature=0`, and a human spot-checks some rows (record the count in `docs/ai-usage.md`).

### 3. Product safety (this assistant)
- Gives hints and cites `file + section`; never outputs a full lab solution. Refusal/attack cases stay in the benchmark.
- Treat student input and retrieved lab files as untrusted data: wrap them in clear tags (e.g. `<student_question>…</student_question>`), keep instructions in the system prompt only.
- Fail loudly: on a model/tool error return an honest "không chắc / không tìm thấy" message and log it to the trace. Never return an empty or made-up answer.
- Stop conditions: any loop has a max step count and a token/cost cap.
- API keys only from `.env` via `codebase/ai.py`; token counts from the API `usage` field, not estimated.

### 4. Simplest first
- One lát cắt (`spec.md` §4). No new framework, service, DB or agent loop without a reason written in `spec.md` §4 and Henry's OK.
- New libraries go in `requirements.txt`. Keep `python run.py` working on Windows.
- Conditional: only if the team adds FastAPI/LangGraph: no blocking I/O in `async def`; no `allow_origins=["*"]` with credentials; keep LangSmith tracing off (`LANGCHAIN_TRACING_V2=false`) while data may contain personal info.

### 5. Git and commits
- Never commit to `main` directly. Branch `feat/<name>-<topic>`, `fix/…`, `docs/…`, `eval/…`, open a PR to `main`, one teammate reviews.
- Work on separate files when possible; announce in the team chat before editing `spec.md` or `AGENTS.md` (high conflict risk).
- Conventional Commits: `<type>(<scope>): <description>`; types `feat fix refactor style test docs chore`; subject ≤ 72 chars (aim < 50), imperative, lowercase, no period. Vietnamese description is fine.
- One logical change per commit; aim 50–200 changed lines, hard cap 400. Exempt: generated run files (`eval/run-N.csv`, `traces/`, `cost/simulate-N.csv`).
- Before each commit: `git diff --staged` (scope, no secrets, no secrets/debug prints), then `python run.py check` must pass.
- Agents never push, merge, force-push or use `--no-verify`. Humans do that.

### 6. Working with Spec-Kit (optional, not before CP2)
- If `.specify/` is added later, its constitution inherits this section; `spec.md` at the root stays the organiser template and the single source of truth.
### 7. Quick facts and decisions (all agents)
- Context for every session: read `docs/checkpoints-context.md` (team, deadlines, Form 2, penalties).
- Product: lab-support assistant for AI20K L3 students (Track A). Hints + `K5-DayXX/FILE#section` citations, never full solutions. Knowledge index: `data/kb_index.json` (built by `data/build_index.py`).
- Stack: Python stdlib only (3.10+). Model call only in `codebase/ai.py`; flow `codebase/agent.py`; tools `codebase/tools.py`.
- Agent-specific files (`CLAUDE.md`, `GEMINI.md`, `.claude/`) are thin pointers to this file. Put shared rules here, never there.
- Decisions: 2026-11-27 Track A, fixed 4-step workflow with 1 LLM call (`spec.md` §4); stdlib framework kept; Spec-Kit deferred until after CP2.
<!-- /team-harness v1 -->
