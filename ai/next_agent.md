# Next Agent

- Current role: `DEV`
- Prompt: `ai/prompts/04-dev.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Handoff Notes

- Active item is `ITEM-0001`: scaffold the Django project baseline under `apps/project-tracker/`.
- Create one Django project and one main `tracker` app only. Do not introduce DRF, extra pip packages, multiple Django apps, or speculative service layers.
- Start with the skeleton in the architecture doc: `manage.py`, `project_tracker/` settings and URLs, `tracker/` app config and URLs, plus `templates/tracker/base.html` and `static/tracker/app.css` / `app.js`.
- Wire SQLite, templates, and static assets in standard Django configuration so later pages can extend the base without rework.
- Provide at least one baseline route and template render so the scaffold is visibly connected end to end.
- Keep future work in mind: later items will add domain models/forms/admin, then dashboard/list/detail/tag pages, then async partial-based CRUD, then tests and validation.
- No clarification or exception was needed. Leave `ai/user-questions.yaml` at `status: none` unless execution uncovers a real blocker.
