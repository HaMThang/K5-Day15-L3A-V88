<<<<<<< HEAD
# CLAUDE.md — team V88
=======
# CLAUDE.md — pointer only

The single source of truth for every coding agent in this repo is `AGENTS.md`. Do not add rules here; edit `AGENTS.md` instead.
>>>>>>> 3062915b69301027f820153200e0a47f2637bfa8

@AGENTS.md
@docs/checkpoints-context.md

<<<<<<< HEAD
## Quick facts
- Product: lab-support assistant for AI20K students (Track A). Hints + `file + section` citations, never full solutions.
- Stack: Python stdlib only (3.10+). Model call lives in `codebase/ai.py`; main flow `codebase/agent.py`; tools `codebase/tools.py`.
- Framework files (do not edit): `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`.

## Commands (mock first, then real)
- `python run.py check` — validate benchmark + metric spec (run before every commit)
- `python run.py eval --fake` — pipeline check, no model call
- `python run.py eval --try` — first 3 cases with the real model
- `python run.py eval` — full run → `eval/run-N.csv` (commit it)
- `python run.py score eval/run-N.csv`
- `python run.py simulate --rate-from eval/run-2.csv` — cost (≥ 50 sessions)
- Add `--wait 4` on free-tier rate limits. macOS/Linux: `python3`.

## Invariants
- `spec.md` §7 threshold + `eval/metric_spec.yaml` locked after Fri 27/11 19:30 (UTC+7).
- Never delete failing cases; never edit finished runs; never commit `.env`.

## Decisions (short ADR log)
- 2026-11-27: Track A, one slice per `spec.md` §4; stdlib framework kept; Spec-Kit deferred until after CP2.
=======
Claude Code only: shared permissions live in `.claude/settings.json` (deny reading `.env`, deny `git push`). Personal overrides go in `.claude/settings.local.json` (git-ignored).
>>>>>>> 3062915b69301027f820153200e0a47f2637bfa8
