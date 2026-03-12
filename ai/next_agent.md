# Next Agent

- Current role: `REVIEWER`
- Prompt: `ai/prompts/06-reviewer.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**

## Active Item

- `ITEM-0008`: document local setup and verification workflow under `apps/project-tracker/`.

## Validator Result

- Validation passed for the revised documentation slice.
- [README.md](/home/sundaram/code/temp/test/apps/project-tracker/README.md) now uses the locked `pyenv` plus Poetry workflow, keeps commands scoped to `apps/project-tracker/`, and preserves the exact `ModuleNotFoundError: No module named 'django'` caveat as an environment/setup issue.
- The current workspace no longer reproduces the earlier missing-Django runtime block: the documented focused Django test command now succeeds in the Poetry environment.

## Validation Evidence

- Passed: `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)`
- Passed: `poetry run python apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` with 36 tests green

## Reviewer Focus

- Confirm the revised README stays within the locked tooling and stack constraints from [goal.yaml](/home/sundaram/code/temp/test/ai/goal.yaml).
- Confirm the documentation remains project-local and accurately reflects the live verification path under [manage.py](/home/sundaram/code/temp/test/apps/project-tracker/manage.py).
- Decide whether the residual assumption about local `pyenv` and Poetry installation is acceptable for closing `ITEM-0008`.
