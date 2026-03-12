# Review Notes

Use this file for reviewer outcomes:

- **DONE**: item accepted and loop returns to PLANNER for next item.
- **REVISE**: route back to specific role with explicit gap list.
- **ESCALATE**: WAITING FOR USER only for approved escalation categories.

## Judgment Warnings

- Flag any introduction of React, Next.js, DRF, extra pip packages, or cloud/deployment scaffolding as scope drift unless requirements are updated.
- Flag architecture that splits the app into speculative layers, services, or multiple Django apps without a demonstrated need.
- Flag CRUD implementations that require full page reloads, since no-reload interactions are part of acceptance.

## Architecture Decisions

- Use a single Django project under `apps/project-tracker/` with one main product app for projects, tasks, and tags.
- Treat server-rendered templates as the primary UI and use small async `fetch` flows for no-reload CRUD interactions.
- Prefer HTML partial responses for mutations; allow narrow JSON responses only when HTML would be more awkward for the specific interaction.
- Keep domain logic in models, forms, and views; reject speculative service, repository, command-bus, or multi-app splits.
- Compute dashboard metrics with direct ORM aggregates against SQLite and avoid extra infrastructure.
