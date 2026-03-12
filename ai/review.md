# Review Notes

Use this file for reviewer outcomes:

- **DONE**: item accepted and loop returns to PLANNER for next item.
- **REVISE**: route back to specific role with explicit gap list.
- **ESCALATE**: WAITING FOR USER only for approved escalation categories.

## Judgment Warnings

- Flag any introduction of React, Next.js, DRF, extra pip packages, or cloud/deployment scaffolding as scope drift unless requirements are updated.
- Flag architecture that splits the app into speculative layers, services, or multiple Django apps without a demonstrated need.
- Flag CRUD implementations that require full page reloads, since no-reload interactions are part of acceptance.
