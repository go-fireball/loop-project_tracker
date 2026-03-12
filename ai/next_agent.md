# Next Agent

- Current role: `ARCHITECT`
- Prompt: `ai/prompts/02-architect.md`
- Execution command for Codex sessions: **Follow `ai/next_agent.yaml` exactly.**
- If role mismatch with `ai/active_agent.txt`, print: `WAITING FOR BATON`

## Handoff Notes

- `ai/simplification.md` now contains explicit guardrails that override conflicting defaults in `ai/judgment.yaml`. Treat Django, SQLite, plain HTML/CSS/JS, and a modular monolith under `apps/project-tracker/` as fixed constraints.
- Do not design a React/Next.js frontend, DRF-style API platform, PostgreSQL deployment, cloud infrastructure, microservices, or speculative multi-app split. Those would be scope drift relative to the product goal.
- Prefer a simple server-rendered Django architecture with small async interactions for no-reload CRUD flows. JSON endpoints are acceptable only when they are the simplest path for a specific interaction, not as a platform layer.
- Keep the domain model direct: projects, tasks, tags, dashboard queries, and the required views only. Avoid repository layers, command buses, plugin systems, or other abstractions unless repeated pain is already visible in the codebase.
- No user clarification was required. `ai/user-questions.yaml` remains `status: none`, and `ai/decision-lock.yaml` is unchanged because there were no answered human decisions to promote.
