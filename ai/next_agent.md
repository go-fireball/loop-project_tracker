# Next Agent

- Current role: `DEV`
- Prompt: `ai/prompts/04-dev.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Handoff Notes

- `ITEM-0003` is accepted and marked done. The next active slice is `ITEM-0004`, narrowed to project-only no-reload CRUD so the async work lands as one coherent vertical cut.
- Backlog change:
  - `ITEM-0004` now covers only project create/update/delete with partial HTML responses and small vanilla JS fetch handlers.
  - `ITEM-0005` now covers task and tag no-reload CRUD after the project interaction pattern exists.
  - `ITEM-0006` remains the automated coverage and final validation slice.
- Implementation target for this turn:
  - Add project mutation routes and views in `apps/project-tracker/tracker/views.py` and `apps/project-tracker/tracker/urls.py`.
  - Reuse `ProjectForm` in `apps/project-tracker/tracker/forms.py`; extend only if the async UX needs form-specific hooks.
  - Introduce reusable project partial templates under `apps/project-tracker/templates/tracker/` for form rendering and replaceable list/detail content.
  - Update existing server-rendered pages, especially `dashboard.html`, `project_list.html`, and `project_detail.html`, to expose create/edit/delete affordances.
  - Expand `apps/project-tracker/static/tracker/app.js` from the current placeholder into minimal fetch-based form handling for partial swaps; keep it framework-free.
  - Adjust `apps/project-tracker/static/tracker/app.css` only as needed to support the new form and inline error states.
  - Add focused mutation coverage in `apps/project-tracker/tracker/tests/test_views.py` for success and invalid-form cases if Django can run; otherwise preserve the missing-Django caveat explicitly.
- Guardrails:
  - Keep everything inside the existing single `tracker` app.
  - Prefer HTML partial responses over JSON.
  - Do not introduce DRF, extra packages, or service/repository layers.
  - Preserve the documented runtime caveat: `manage.py test` is still expected to fail in this workspace until Django is installed.
