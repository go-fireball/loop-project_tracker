# Next Agent

- Current role: `DEV`
- Prompt: `ai/prompts/04-dev.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Active Item

- `ITEM-0008`: document local setup and verification workflow under `apps/project-tracker/`.
- Keep the slice implementation-only and lightweight: this is a documentation closeout task, not new feature work.

## Implementation Notes

- Add `apps/project-tracker/README.md` with concrete local setup steps for creating a Python environment, installing Django, applying migrations, running the dev server, and executing the accepted focused test commands.
- Keep the commands aligned with the current project entrypoint and test surface:
  - `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)`
  - `python3 apps/project-tracker/manage.py migrate`
  - `python3 apps/project-tracker/manage.py runserver`
  - `python3 apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views`
- Preserve the known runtime caveat explicitly: the current workspace still fails Django commands with `ModuleNotFoundError: No module named 'django'`.
- Frame that caveat as an environment/setup limitation rather than a tracker application defect.

## Guardrails

- Stay inside `apps/project-tracker/` unless a small supporting adjustment is required for documentation accuracy.
- Do not introduce new packages beyond Django or expand scope into more product code unless the docs are inaccurate without a minimal correction.
- Keep the documented stack consistent with the locked architecture: Django, SQLite, server-rendered templates, and vanilla JS.

## Verification Expectation

- Re-run `py_compile` after the documentation change if practical.
- Attempt the Django test command only if the environment permits it; if it still fails because Django is absent, keep that evidence in the handoff to validator.
