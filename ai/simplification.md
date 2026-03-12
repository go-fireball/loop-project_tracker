# Simplification Guidance

1. Keep the system as a single Django project under `apps/project-tracker/`, with a straightforward modular monolith structure.
2. Prefer Django built-ins first: ORM models, forms where useful, template rendering, URL routing, migrations, and standard views before introducing custom infrastructure.
3. Treat the HTML/vanilla-JS UI as the product surface. Use small asynchronous endpoints or partial-template responses only to avoid full page reloads.
4. Do not introduce a separate SPA, frontend framework, public REST platform, or client-state architecture. The goal is fast CRUD, not a reusable API product.
5. Use SQLite-specific pragmatism. Avoid designs that require database features, concurrency assumptions, or deployment topology beyond a local Django app with SQLite.
6. Keep the domain model direct: projects, tasks, and tags only. Add helper services or abstraction layers only when duplication is concrete and repeated.
7. Favor one Django app unless a second app is clearly required by code boundaries that already exist. Do not split by speculative future scale.
8. Keep interfaces small and explicit. Prefer clear view/template/form boundaries over generic repositories, command buses, or plugin systems.
9. Preserve required business behavior exactly, especially statuses, priorities, relationships, dashboard counts, and no-reload CRUD interactions.
10. Record tradeoffs in design docs when choosing between template-partial updates and JSON responses, but default to the simpler implementation that satisfies the acceptance criteria.

## Judgment Guardrails

- Override conflicting defaults from `ai/judgment.yaml`: this project is Django, SQLite, plain HTML/CSS/JS, and a single deployable app, not ASP.NET, React/Next.js, PostgreSQL, or AWS-first infrastructure.
- Avoid cloud, container, auth, queueing, CDN, object storage, and microservice concerns unless the requirements explicitly add them later.
- Keep human escalation reserved for genuine product tradeoffs. Routine engineering choices should be resolved in favor of the simplest maintainable implementation.
- Architecture should optimize for easy local development, readable server-rendered flows, and testable CRUD behavior, not for hypothetical multi-user or distributed futures.

## Tradeoff Notes

- If partial page updates can be done with server-rendered HTML fragments, prefer that over designing a broad JSON API.
- If a choice exists between a reusable abstraction and a slightly repetitive but obvious implementation, prefer the obvious implementation first.
- If dashboard logic can be computed with direct ORM queries, do not add caching or analytics layers.
