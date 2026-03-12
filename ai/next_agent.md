# Next Agent

- Current role: `PLANNER`
- Prompt: `ai/prompts/03-planner.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Handoff Notes

- The architecture baseline is documented in `context/repo/architecture.md`.
- Keep the implementation as one Django project under `apps/project-tracker/` with one main product app rather than splitting into multiple Django apps or platform layers.
- Plan around server-rendered pages plus small async CRUD interactions. Prefer HTML partial responses for create, update, and delete flows; use JSON only where a partial would be needlessly awkward.
- The planner should turn this into incremental items that establish project scaffolding first, then domain models/forms/admin, then page views/templates, then no-reload interaction wiring, then tests/validation.
- Required user-facing views are dashboard, project list, project detail with tasks, and tag filter/detail.
- Core model surface is intentionally small: `Project`, `Task`, and `Tag` with direct Django ORM relationships and SQLite-backed aggregates for dashboard counts.
- No clarification or exception was needed. `ai/user-questions.yaml` remains `status: none`, and `ai/decision-lock.yaml` remains unchanged.
