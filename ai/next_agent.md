# Next Agent

- Current role: `PLANNER`
- Prompt: `ai/prompts/03-planner.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**

## Handoff Summary

- Reviewer accepted the idle completion handoff as `DONE`; this is still a completion-state baton pass, not a reopened implementation slice.
- `ai/active_item.yaml` remains idle and now points ownership back to `PLANNER` because every backlog item in `ai/backlog.yaml` is already `done`.
- The current turn only updates baton-state files under `ai/`; there is still no application diff under `apps/` or `infra/`.

## Accepted Validation Context

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed in the current Poetry environment.
- `poetry run python apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` passed with 36 tests.
- No new regressions were introduced because this handoff did not change application code.

## Planner Focus

- Preserve the explicit project-complete state unless new user scope appears.
- Do not invent a new backlog item or implementation slice without new requirements, a recorded exception, or direct user direction.
- Keep the standing repository-hygiene caveat visible: rerunning `py_compile` can transiently regenerate local `__pycache__` directories under `apps/project-tracker/`.
