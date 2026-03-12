# Next Agent

- Current role: `DEV`
- Prompt: `ai/prompts/04-dev.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**

## Handoff Summary

- `ITEM-0008` is accepted and marked done.
- Planning has activated `ITEM-0009` as a small repository-hygiene follow-up already called out in prior review notes: remove tracked Python bytecode artifacts from `apps/project-tracker/`.
- Keep the existing locked stack and behavior unchanged. This slice is cleanup only, not feature work.

## Active Item

- `ITEM-0009` Remove tracked Python bytecode artifacts
- Goal: clean tracked `__pycache__` directories and `.pyc` files from `apps/project-tracker/` so the repository reflects source-controlled Django code only.

## DEV Focus

- Delete tracked bytecode artifacts under:
  - `apps/project-tracker/__pycache__/`
  - `apps/project-tracker/project_tracker/__pycache__/`
  - `apps/project-tracker/tracker/__pycache__/`
  - `apps/project-tracker/tracker/migrations/__pycache__/`
  - `apps/project-tracker/tracker/tests/__pycache__/`
- Do not modify source files, templates, static assets, or docs for this slice.
- Re-run:
  - `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)`
  - `poetry run python apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views`
- Record cleanup and verification evidence in `ai/review.md`, then hand off to VALIDATOR.
