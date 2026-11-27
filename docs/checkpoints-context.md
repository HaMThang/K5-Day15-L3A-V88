# Checkpoints context — team V88 (read this first)

> TL;DR: AI20K hackathon, Day15, class L3A, team V88, Track A (EdTech). 4 checkpoints (15 pts total, late = 0) submitted via Form 2 by the lead; repo locks Sat 28/11 23:59 (UTC+7).
> For agents: this file is context, not a task list. Repo files (`README.md`, `AGENTS.md`, `spec.md`) win over this file when they differ; report the `file:line` conflict instead of guessing.

Last updated: 2026-11-27 12:50 UTC+7 · Owner: Lê Gia Hưng · All times are UTC+7.

## 1. Team

| Role | Name | MSSV | Owns |
|---|---|---|---|
| Lead | Lê Gia Hưng | 2A202603706 | coordination, `spec.md`, `canvas.md`, pitch, Form 2 submissions |
| Member | Nguyễn Thế Hoàng | 2A202603718 | `codebase/` (agent, tools, model call) |
| Member | Đặng Đức Cương | 2A202603680 | `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/report.md` |
| Member | Hà Minh Thắng | 2A202603676 | evidence: pre-class data mining, interviews, `evidence/` |

- Repo: https://github.com/HaMThang/K5-Day15-L3A-V88 (public; owner Thắng). Source of truth for names/IDs: `TEAMS.md` (organisers scan it; keep its format).

## 2. Problem and slice (locked, from `canvas.md`)
- Track A · A6 lab support. Assistant that answers lab/hackathon requirement questions with the exact `file + section` source, hints the next step, never does the work.
- User: an AI20K L3 student doing a lab/hackathon spread across many files (checkpoints, rubric, rules, guide, track file).
- Pain (no word "AI"): students open many files at once to know what to submit and what counts as passing, lose time searching and miss requirements, then lose checkpoint points.
- One-sentence slice: one student · asks "what does this checkpoint need / has our part passed" · the assistant decides between answering with file code + section, or "not in the documents, ask the lab coach" · the student opens the right section, checks it themselves, knows the next step, gets no ready-made work.
- Autonomy: read docs + cited answer only. No writing submissions, no repo edits, no submitting. No source / conflicting files / "do it for me" → refuse and point to the lab coach.
- Course data (verified counts, `data/preclass/events.csv` of the organiser repo): 602 `lab_opened` (147 learners), 453 `lab_completed` (123 learners), 102 completed with `skipped=true` (22.5%); only 14 of 1,260 `chat_sent` carry a `lab_key`.

## 3. Form 2 (how every checkpoint is submitted)
- Field "MSSV Đội trưởng": `2A202603706`, exactly as in Form 1, no spaces.
- Field "Bạn đang nộp mốc Checkpoint nào?": pick one of the 4 options in §4.
- Following pages differ per checkpoint (CP1 asks for: problem statement without the word "AI", the one-sentence slice, and confirmation that `TEAMS.md`/`canvas.md` are pushed and `python run.py check` is clean). Fields of later pages: CHƯA KIỂM; record them here once seen.

## 4. Checkpoints

| CP | Deadline | Pts | Form label | Status |
|---|---|---|---|---|
| CP1 | Fri 27/11 17:00 | 3 | TEAMS, 6 Track, Canvas & Repo mới | repo moved to root and pushed (commit `1592568`); form submission: CHƯA KIỂM |
| CP2 | Fri 27/11 19:30 | 4 | Spec, Benchmark ≥10 & CHỐT chuẩn đạt | open |
| CP3 | Sat 28/11 10:00 | 4 | Evidence, Video 30s AI thật & Lượt 1 | open |
| CP4 | Sat 28/11 14:30 | 4 | Lượt 2, Chi phí, Slide PDF & 4 ĐK xét giải | open |

### CP1 — Fri 17:00 (3 pts)
- Public repo named `K5-Day15-L3A-V88`, starter files at root (`README.md`, `run.py` on the front page); link opens in an incognito window.
- `TEAMS.md`: lead on row 1; `python run.py check` shows no warning under "Kiểm TEAMS.md". Members invited as collaborators.
- `canvas.md`: 7 rows filled, problem without the word "AI", exactly 1 of the 6 tracks.

### CP2 — Fri 19:30 (4 pts) · THRESHOLD LOCK
- `spec.md` §4 architecture diagram/design.
- `eval/benchmark.csv` ≥ 10 cases (columns `id,input,expected,pass_criterion,type,source`; types `thuong|kho|tu_choi`).
- `eval/metric_spec.yaml` ≥ 3 metrics, each with name · definition · grader · threshold.
- `data/DATA_CARD.md` first version.
- `python run.py` runs end to end (fake/mock model is fine before CP2).
- `spec.md` §7: numeric pass threshold ("Đạt khi ≥ __% câu qua, và __"). **After 19:30 never change §7 or `metric_spec.yaml`.**
- `canvas.md`: update row 4 with first numbers + 1 quote, fill "Đã đổi gì so với CP1".

### CP3 — Sat 10:00 (4 pts)
- `evidence/summary.md`: ≥ 1 source, ≥ 5 verbatim quotes (no invented people/quotes).
- Benchmark 20–30 cases: ≥ 5 `kho`, ≥ 2 `tu_choi` including attack/prompt-injection cases; ≥ 1/3 of cases with `source` from real users or real data (`nguoi_dung` / `data_that`).
- Real model connected (`docs/connect-model.md`); `python run.py eval --try` shows tokens > 0.
- `python run.py eval` → run 1: `eval/run-1.csv` + `traces/run-1.jsonl` (commit both; fill `pass`).
- 30 s video of the real AI running (unlisted link; check it opens in incognito).
- `spec.md` §0–§7 complete.

### CP4 — Sat 14:30 (4 pts)
- Improve, then run 2: `eval/run-2.csv`; `eval/report.md` compares run 1 vs run 2 (honest low results still score; edited/hidden numbers score 0).
- `python run.py simulate --rate-from eval/run-2.csv` with ≥ 50 sessions → `cost/simulate-N.csv`; `cost/cost-estimate.md`, `spec.md` §8.
- Slides at repo root as `demo-slides.pdf` + backup video link. Note: organiser commit `6225f90` (27/11 09:11) relaxed the format to PDF/PPTX/HTML/link and repo `README.md` §7 says the same, but the Form label still says "Slide PDF" → ship PDF to be safe.
- Tick the 4 hard conditions on the form (§5).
- Bonus: `validation/log.md` (real user tried it).

## 5. Four hard conditions to be eligible for prizes (checked at CP4)
1. Real AI call at the central decision (not fake mode).
2. Pain evidence meets the rubric threshold (R1; synthetic data, teammates or AI personas do not count; R1 capped at 5/14 otherwise).
3. ≥ 20 test cases with a % pass result.
4. Slides (+ demo, backup video).

## 6. Never (penalties)
- Commit API keys/`.env` or real personal data → −10. Raw organiser data stays in `data-btc/` (git-ignored).
- Change the pass threshold after CP2, delete failing cases, or edit `expected` to match output → that block scores 0.
- Edit finished runs (`eval/run-N.csv`, `cost/simulate-N.csv`, `traces/`) except the `pass`/`ghi_chu` columns.
- Invent interviewees, quotes, survey answers or numbers; unsourced numbers are marked *(tự ước tính)*.
- Not being able to explain a part with your name on it → that part scores 0 (`docs/ai-usage.md`).

## 7. Saturday 28/11 schedule and repo lock
- 10:00 CP3 · 14:30 CP4.
- Demo Zone 14:30–16:00: 5 min pitch + 3 min Q&A.
- Final 16:00–18:00: 6 min pitch + 5 min Q&A. Prizes +10 / +7 / +5 lab points.
- 23:59 repo lock: `spec.md` §10 (assignments + changelog), `reflection/<name>.md` for all 4 members, `docs/ai-usage.md` filled, README "Dùng AI vào việc gì".

## 8. Scoring (from rubric, via team research)
- 15 on-time pts (CP1 3 · CP2 4 · CP3 4 · CP4 4) + 85 graded + 5 bonus.
- Heaviest blocks: R1 pain 14 · R2 impact 11 · R4 cases/metrics 14 · R5 eval report 8 · R6 cost 12 (= 59/85). R3 design + prototype 16; number of tools earns nothing.

## 9. Where to read more
- `README.md` (repo) — commands, which file is due at which checkpoint, 7 mandatory items.
- `AGENTS.md` — rules for coding agents. `docs/team-setup-prompt.md` — team Claude Code setup.
- `docs/research/draft-answers.md` — unreviewed drafts for `spec.md`, `metric_spec.yaml`, 15 draft benchmark cases (cites organiser commit `6225f90`).
- `docs/research/why-not-chatgpt.md` — differentiation vs ChatGPT, for `spec.md` §3 and Q&A.
- Organiser repo (not committed here): `README.md`, `02-guide.md`, `03-rubric.md`, `tracks/track-a-edtech.md`.
