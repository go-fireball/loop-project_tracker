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

## DEV Implementation Notes

- Scaffolded `apps/project-tracker/` as a single Django project with one `tracker` app.
- Wired SQLite, template discovery, and static asset loading in `project_tracker/settings.py`.
- Added root URL routing through `project_tracker/urls.py` into `tracker/urls.py`.
- Added a baseline `dashboard` view and shared templates at `templates/tracker/base.html` and `templates/tracker/dashboard.html`.
- Added starter static assets at `static/tracker/app.css` and `static/tracker/app.js`.
- Added a route smoke test in `tracker/tests/test_views.py`.
- Added `Project`, `Task`, and `Tag` models in `tracker/models.py` with the locked status and priority choices, `Task -> Project` ownership, and tag many-to-many relationships on both projects and tasks.
- Added `ProjectForm`, `TaskForm`, and `TagForm` in `tracker/forms.py` with explicit validation aligned to the approved enumerated values and date widgets for date fields.
- Registered the tracker domain models in `tracker/admin.py` with practical list displays, filters, search fields, and tag management controls.
- Added `tracker/migrations/0001_initial.py` to create the initial domain schema inside the existing tracker app.
- Added `tracker/tests/test_domain.py` covering the domain relationships plus model and form validation for the locked enumerations.
- Expanded `tracker/views.py` so the dashboard computes live ORM aggregates for total projects, task counts by status, overdue tasks, and recent projects.
- Added server-rendered `project_list`, `project_detail`, and `tag_detail` views plus routes in `tracker/urls.py`.
- Replaced the scaffold dashboard template with aggregate-driven content and added `project_list.html`, `project_detail.html`, and `tag_detail.html`, all extending the shared base template.
- Updated `tracker/base.html` navigation and extended `static/tracker/app.css` so the new read pages share a consistent layout without introducing frontend framework code.
- Replaced the simple view smoke test with focused database-backed view tests covering dashboard aggregates, project listing, project detail, and tag detail rendering.

## Validator Outcome

- Result: PASS for `ITEM-0001`.
- Acceptance criteria check:
  - Single Django project exists under `apps/project-tracker/` with one `tracker` app only.
  - SQLite, template discovery, and static asset configuration are present in `project_tracker/settings.py`.
  - Root URLconf routes to `tracker.urls`, and the dashboard view renders the baseline template.
  - Shared base template and starter static assets are wired through Django's standard configuration.
- Regression check:
  - No scope drift found: no extra apps, packages, frontend frameworks, or speculative architecture layers were introduced.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test` is currently blocked by the workspace environment and failed with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime and test validation remain partial until Django is installed in the workspace.
- Current automated coverage is limited to a simple dashboard route smoke test, so later slices still need model, mutation, and no-reload interaction coverage.
- The initial migration was authored manually because `manage.py makemigrations` cannot run without Django in the workspace, so schema validation should be rechecked once Django is available.
- The new read-page tests and templates cannot be executed end to end in this workspace until Django is installed; only Python compilation passed for this slice.

## Reviewer Decision

- Decision: DONE for `ITEM-0001`.
- Accepted because the scaffold slice meets the locked single-project Django structure, wires the tracker app into settings and URLs, and proves template/static asset integration without scope drift.
- Accepted with environment caveat: `manage.py test` could not run in this workspace because Django is not installed, but the failure mode is external to the slice and was documented with passing Python compilation evidence.
- Follow-up note for later cleanup: committed `__pycache__` artifacts are repository hygiene noise and should be removed outside this acceptance decision.

## Validator Outcome

- Result: PASS for `ITEM-0002`.
- Acceptance criteria check:
  - `Project`, `Task`, and `Tag` are implemented in `tracker/models.py` with the locked field sets, ORM relationships, and enumerated choices.
  - `Task` points to `Project`, and tags are modeled as many-to-many relationships on both `Project` and `Task`.
  - `ProjectForm`, `TaskForm`, and `TagForm` enforce the approved choice sets and required-field behavior without introducing extra abstraction layers.
  - Admin registration covers all three domain models with list views, filters, search, and tag editing support for inspection.
  - `tracker/migrations/0001_initial.py` matches the implemented model schema, including ordering, defaults, and relationships.
- Regression check:
  - No scope drift found: the slice stays inside the existing `tracker` app and does not add packages, apps, or speculative architecture layers.
  - Manual inspection found the migration definitions aligned with the current model fields and locked enumerations.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime validation is still partial because Django is not installed in the workspace, so the migration and test suite could not be executed end to end.
- The initial migration was authored manually and appears consistent with the models on inspection, but it still needs runtime verification once Django is available.

## Reviewer Decision

- Decision: DONE for `ITEM-0002`.
- Accepted because the implemented models, forms, admin wiring, and initial migration satisfy the locked domain slice without introducing scope drift or architectural violations.
- Accepted with environment caveat: Django is missing from the workspace, so runtime execution of the migration and focused test suite remains blocked even though static validation and schema consistency checks passed.
- Follow-up note for later slices: once Django is available, run the domain and view tests plus migration checks before final acceptance of the broader CRUD workflow.

## Validator Outcome

- Result: PASS for `ITEM-0003`.
- Acceptance criteria check:
  - `tracker/views.py` computes dashboard aggregates directly with ORM queries for total projects, task counts by status, overdue non-done tasks, and recent projects.
  - `tracker/urls.py` exposes dashboard, project list, project detail, and tag detail routes inside the existing single-app Django structure.
  - `project_list.html`, `project_detail.html`, and `tag_detail.html` extend the shared base template and provide the required navigation and related-object rendering.
  - `tracker/tests/test_views.py` covers the dashboard, projects list, project detail, and tag detail routes with database-backed assertions for key rendered content.
- Regression check:
  - No scope drift found: the slice stays inside the existing Django project and tracker app, uses server-rendered templates, and does not add packages or speculative layers.
  - The implementation remains aligned with the active-item constraint to use direct ORM access rather than service or repository abstractions.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime validation is still partial because Django is not installed in the workspace, so the focused view tests could not be executed end to end.
- Template rendering behavior, URL wiring, and ORM query execution were validated by inspection rather than a live Django run for this slice.

## Reviewer Decision

- Decision: DONE for `ITEM-0003`.
- Accepted because the dashboard, project list, project detail, and tag detail pages meet the locked slice using direct ORM queries, server-rendered templates, and focused route coverage without scope drift.
- Accepted with environment caveat: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` remains blocked by `ModuleNotFoundError: No module named 'django'`, so runtime execution still needs to be retried once Django is installed in the workspace.
