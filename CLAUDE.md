# CLAUDE.md — pointer only

The single source of truth for every coding agent in this repo is `AGENTS.md`. Do not add rules here; edit `AGENTS.md` instead.

@AGENTS.md
@docs/checkpoints-context.md

Claude Code only: shared permissions live in `.claude/settings.json` (deny reading `.env`, deny `git push`). Personal overrides go in `.claude/settings.local.json` (git-ignored).
