# Handoff Notes — SENIOR_JUDGMENTAL_ENGINEER → ARCHITECT

- Current role: `ARCHITECT`
- Prompt: `ai/prompts/02-architect.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Judgment outcome

The scope is valid as written. Nothing needs escalation and nothing important is missing for the stated personal-use tracker. The goal-level stack requirement overrides `judgment.yaml` defaults: use Django, SQLite, and vanilla JS only.

## Guardrails now in force

1. Keep this as a small modular monolith inside `apps/project-tracker/`; do not split into multiple Django apps or invent services/repositories.
2. Use plain Django views for JSON CRUD. No DRF, no class-heavy abstraction, no generic CRUD framework.
3. Keep page-rendering views and JSON endpoints separate. Templates serve pages; fetch hits JSON routes.
4. Use direct ORM queries plus simple aggregation for dashboard stats. No raw SQL unless architecture uncovers a real blocker.
5. Tag filtering only needs a single selected tag to satisfy scope. Do not broaden to advanced search.
6. Status/priority enums should be centralized with Django `TextChoices`.

## What architecture needs to pin down

1. Django project/app layout under `apps/project-tracker/`, including where templates, static files, and URL modules live.
2. Model design for `Project`, `Task`, and `Tag`, including the two many-to-many relationships for tags.
3. URL boundary between HTML views and JSON endpoints, keeping the route map flat and readable.
4. The minimum frontend data flow needed for async create/update/delete without full page reload.
5. Dashboard query approach for total projects, task counts by status, and overdue tasks using timezone-aware date logic.

## Risks to watch

- The async mutation requirement is firm. Architecture should make the JS/API contract explicit enough that DEV does not fall back to form-post/full-refresh behavior.
- The no-third-party-packages constraint means any admin-style convenience abstractions are out. Keep the design intentionally simple.
- `ai/active_item.yaml` is still idle/null, so architecture should stay at whole-system design level and avoid pretending a narrower implementation slice has already been chosen.

## Next role after you

PLANNER — after the architecture and boundaries are defined.
