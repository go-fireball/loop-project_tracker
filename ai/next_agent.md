# Next Agent

- Current role: `SENIOR_JUDGMENTAL_ENGINEER`
- Prompt: `ai/prompts/01-senior-judgmental-engineer.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Handoff Notes

- Refined `ai/requirements.md` from the project goal into a concrete one-pager covering objective, scope, explicit non-goals, constraints, and testable acceptance criteria.
- No user clarification was required. `ai/user-questions.yaml` remains `status: none`, and `ai/decision-lock.yaml` is unchanged because there were no answered questions to promote.
- Focus judgment on keeping the implementation lean: single Django app flow, built-in Django capabilities only, vanilla JS for partial updates, and no speculative platform concerns.
- Watch for default engineering preferences in `ai/judgment.yaml` that conflict with the explicit project goal; the goal already fixes Django, SQLite, and plain HTML/JS.
