# Handoff Notes — PRODUCT_OWNER → SENIOR_JUDGMENTAL_ENGINEER

- Current role: `SENIOR_JUDGMENTAL_ENGINEER`
- Prompt: `ai/prompts/01-senior-judgmental-engineer.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## What was done

`ai/requirements.md` has been fully written from `ai/goal.yaml`. The goal was unambiguous and complete — no open questions were raised and no user clarification was needed.

## What to focus on

1. **Stack divergence from judgment.yaml defaults** — `judgment.yaml` defaults to `aspnet_core` backend and `react_nextjs` frontend, but the goal explicitly mandates Django + vanilla JS. This is a goal-level override; no exception entry is needed in `decision-lock.yaml` unless you disagree.
2. **Constraint strictness** — "no additional pip packages" rules out DRF. The implementation must use plain Django views for the JSON API. Confirm this is achievable and flag if any hidden complexity makes it risky.
3. **Scope tightness** — no auth, no file uploads, no email. The scope is deliberately narrow. Validate nothing important has been omitted that would make the tracker unusable for the stated personal-use goal.
4. **Async mutation requirement** — add/edit/delete without full page reload using vanilla JS fetch. This is a firm UX requirement, not optional.

## Concerns / risks

- None blocking. The goal is explicit and the requirements are a direct translation.
- Watch for scope creep: the dashboard and tag-filter view are included in scope — both must be covered.

## Next role after you

ARCHITECT — who will design the Django project structure, model layout, URL routing, and view/API boundary.
