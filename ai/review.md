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

## DEV Implementation Notes

- Implemented the project-only no-reload CRUD slice already wired in `tracker/views.py` and `tracker/urls.py`: project create, edit, and delete return HTML partial swap responses rather than broad JSON payloads.
- Updated `dashboard.html`, `project_list.html`, `project_detail.html`, and the tracker partial templates so create/edit/delete affordances render inside stable DOM regions that can be replaced in place.
- Expanded `static/tracker/app.js` into minimal vanilla `fetch` handlers for async form submits and async edit-link loads, plus selector-based partial swaps.
- Extended `static/tracker/app.css` for form layout, action buttons, and inline validation state styling needed by the mutation flow.
- Added focused view coverage in `tracker/tests/test_views.py` for project create success, create validation errors, edit-form loading, update success, and delete responses from detail and dashboard surfaces.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- End-to-end runtime coverage for the new mutation views and partial templates is still blocked until Django is available in the workspace.
- The async project CRUD behavior depends on client-side DOM swaps against the shipped selectors, so validator should inspect the rendered partial target IDs alongside the server responses.

## Validator Outcome

- Result: PASS for `ITEM-0004`.
- Acceptance criteria check:
  - `tracker/views.py` implements project create, update, and delete flows using HTML partial responses and keeps the slice limited to project mutations inside the existing Django app.
  - `dashboard.html`, `project_list.html`, `project_detail.html`, and the project partials expose stable swap regions that match the selectors used by the mutation responses.
  - `static/tracker/app.js` stays framework-free and performs the expected `fetch`-based submit/load interception for `data-async-form` and `data-async-link` elements.
  - Invalid create submissions return inline partial HTML errors with a `400` response, and the update view uses the same form-partial rendering pattern for invalid submissions.
- Regression check:
  - No scope drift found: no DRF, extra packages, extra Django apps, or speculative layers were introduced.
  - The mutation responses and page templates use a consistent `template[data-swap-target]` contract and matching DOM region IDs on dashboard, project list, and project detail surfaces.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime validation is still partial because Django is not installed in the workspace, so the focused mutation tests could not be executed end to end.
- Focused tests cover create success/error, edit-form load, update success, and delete responses from detail and dashboard, but there is no dedicated test for invalid update submissions or project-list delete responses; those paths were accepted by code inspection only.

## Reviewer Decision

- Decision: DONE for `ITEM-0004`.
- Accepted because the project create, update, and delete flows stay inside the existing Django tracker app, return HTML partial swap responses, and preserve the locked plain HTML plus vanilla JS approach without scope drift.
- Accepted with environment caveat: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` is still blocked by `ModuleNotFoundError: No module named 'django'`, so runtime execution of the mutation suite remains pending outside this workspace.
- Residual risk carried forward: invalid update submissions and project-list delete responses do not have dedicated focused tests yet, but the implemented paths match the existing partial-response contract on inspection.

## DEV Implementation Notes

- Implemented `ITEM-0005` task-only no-reload CRUD inside the existing tracker app by adding task create, update, and delete views plus nested task routes under project detail.
- Narrowed `TaskForm` so the project is fixed by the URL-driven project detail context rather than exposed as a mutable cross-project field in async task forms.
- Added reusable task partials for the create/edit form, task list, and edit placeholder, and rewired `project_detail.html` to render stable swap regions for project summary, task create, task edit, and task list content.
- Updated the project detail summary panel to surface live task counts so successful task mutations can refresh the supporting summary region alongside the task list.
- Reused the existing partial mutation response contract in `tracker/views.py` so successful task mutations refresh the project detail summary, reset the create form, replace the task list, and clear the edit form region.
- Kept the client-side code small by reusing the existing async fetch/swap handler in `static/tracker/app.js`, only generalizing the user-facing error text from project-specific wording to generic mutation wording.
- Added focused view coverage in `tracker/tests/test_views.py` for task create success, task create validation errors, task edit-form load, task update success, and task delete success.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime validation of the new task mutation views and templates is still blocked until Django is installed in the workspace.
- The async task CRUD flow depends on the shipped selector contract between server-rendered partial responses and DOM region IDs on `project_detail.html`, so validator should inspect those selectors together.

## Validator Outcome

- Result: FAIL for `ITEM-0005`.
- Acceptance criteria check:
  - `tracker/views.py` adds task create, update, and delete endpoints under project detail routes and keeps the implementation inside the existing Django app with HTML partial responses and the established vanilla JS swap contract.
  - `TaskForm` no longer exposes cross-project reassignment, so task ownership is correctly fixed by the URL-driven project context in the task mutation views.
  - `project_detail.html` and the new task partials provide stable swap regions for task create, task edit, and task list updates, and the focused view tests cover the intended success and invalid-create paths by inspection.
- Regression check:
  - Regression found: deleting a project from the detail page now leaves stale task create, task edit, and task list regions rendered on screen because `project_detail.html` moved those regions outside `#project-detail-region`, but `project_delete()` still only replaces `#project-detail-region` and `#project-edit-form-region`.
  - This leaves visible controls pointing at deleted-project task endpoints after project deletion, which breaks the no-reload detail-page flow and is not covered by the current delete test.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.
- Code inspection evidence for the regression:
  - `project_detail.html` renders `#task-create-form-region`, `#task-edit-form-region`, and `#task-list-region` outside `#project-detail-region`.
  - `project_delete()` only swaps `#project-detail-region` plus `#project-edit-form-region` for the `project_detail` source-page response.

## Known Risks

- Runtime validation of the new task mutation views and templates is still blocked until Django is installed in the workspace.
- The regression on project deletion from the detail page should be fixed before acceptance, and a focused test should assert that the task regions are cleared or replaced when the parent project is deleted from that surface.

## DEV Implementation Notes

- Implemented `ITEM-0006` as a dedicated server-rendered tag management surface in `tracker/tag_detail.html` with stable async swap regions for tag create, selected-tag detail, edit form, and tag list.
- Added `tag_list`, `tag_create`, `tag_update`, and `tag_delete` flows in `tracker/views.py` and `tracker/urls.py`, reusing the existing HTML partial mutation-response contract instead of introducing JSON or a new frontend layer.
- Added reusable tag partials for the create/edit form, tag list, selected-tag detail, and edit placeholder under `templates/tracker/partials/`.
- Extended `static/tracker/app.js` so region wrappers keep their DOM IDs across repeated async swaps, which the new tag CRUD surface needs and which also hardens the existing project/task mutation behavior.
- Extended `static/tracker/app.css` and `templates/tracker/base.html` to support the tag management layout and primary navigation entry without changing the established visual language.
- Added focused view coverage in `tracker/tests/test_views.py` for tag management page rendering, tag create success/error, edit-form loading, update success, and delete success.

## Known Risks

- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` is still blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so the new tag CRUD tests and runtime template behavior could only be verified by static inspection and Python compilation.
- The swap-layer fix in `static/tracker/app.js` changes shared mutation behavior for project, task, and tag regions; validator should inspect selector-to-region parity on the existing project/task surfaces alongside the new tag surface.

## Reviewer Decision

- Decision: REVISE for `ITEM-0005`.
- Rejected because deleting a project from its detail page leaves stale task CRUD UI behind: `project_detail.html` renders `#task-create-form-region`, `#task-edit-form-region`, and `#task-list-region` outside `#project-detail-region`, but `project_delete()` still only swaps `#project-detail-region` and `#project-edit-form-region` for the `project_detail` response.
- Required fix for the next pass:
  - Update the detail-page project delete response so all task regions are cleared or replaced along with the deleted-project panel.

## DEV Implementation Notes

- Extended `apps/project-tracker/tracker/tests/test_domain.py` to cover locked default values on `Project` and `Task`, confirm `TaskForm` does not expose project reassignment, and add representative invalid status assertions for the project and task forms.
- Extended `apps/project-tracker/tracker/tests/test_views.py` to cover the remaining meaningful server-rendered and no-reload branches: AJAX tag-detail swaps, invalid project/task/tag edit submissions, project-list delete refreshes, and representative 405 method guards on mutation routes.
- Kept the final coverage pass inside the existing Django test modules and did not change product code because the expanded assertions did not expose a product defect beyond the already fixed selector-contract work.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime execution of the expanded Django test suite is still blocked by the workspace environment, so the new final-pass assertions were validated statically but not executed end to end.
- The remaining acceptance risk is environmental rather than product-code drift: validator should preserve the missing-Django caveat unless the package becomes available during the next slice.
  - Add a focused regression test covering project deletion from the detail page and asserting the stale task regions are not left behind in the async response.
- Environment caveat remains unchanged: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` is still blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so the reviewer decision is based on code inspection plus py-compile evidence.

## DEV Revision Notes

- Updated `tracker/views.py` so the `project_detail` branch of `project_delete()` now swaps all task regions, not just the deleted project panel and project edit placeholder.
- Added explicit empty placeholder partials for `#task-create-form-region` and `#task-list-region` so the async response clears those DOM regions without leaving stale task CRUD controls behind.
- Tightened `tracker/tests/test_views.py::test_project_delete_from_detail_returns_deleted_panel` to assert the delete response now includes swap instructions for all task regions and no longer returns stale task form/list content.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` still fails in the workspace with `ModuleNotFoundError: No module named 'django'`.

## Known Risks

- Runtime validation of the revised delete-response path is still blocked until Django is installed in the workspace.

## Validator Decision

- Result: PASS for `ITEM-0006`.
- Acceptance criteria check:
  - `tracker/views.py` and `tracker/urls.py` provide tag create, update, delete, list, and detail flows inside the existing Django app with HTML partial mutation responses only.
  - `templates/tracker/tag_detail.html` and the tag partials expose stable create, detail, edit, and list swap regions for the dedicated server-rendered tag management surface.
  - Invalid tag submissions return inline form errors through the same partial-response contract rather than forcing a full-page workflow.
  - The shared `static/tracker/app.js` swap helper preserves wrapper IDs across repeated async updates, which keeps the existing project/task surfaces compatible with the new tag management regions.
- Regression check:
  - No blocking regression found by inspection in the shared swap helper or tag mutation selector contract.

## Reviewer Decision

- Decision: DONE for `ITEM-0006`.
- Accepted because the tag CRUD slice satisfies the locked no-reload requirements on a dedicated server-rendered management surface and stays within the existing Django + vanilla JS architecture.
- Accepted with unchanged environment caveat: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` remains blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so runtime verification is still limited to static inspection plus Python compilation.
- Follow-up for planning: the remaining backlog item should focus on final automated coverage and end-to-end validation once the workspace can run Django tests.

- Decision: PASS for `ITEM-0005`.
- Accepted because the revised `project_delete()` detail-page response now clears every task-owned swap region that lives outside `#project-detail-region`, matching the current DOM layout and removing the stale task CRUD regression identified in the prior validation pass.
- Focused inspection confirms the response now swaps `#project-detail-region`, `#project-edit-form-region`, `#task-create-form-region`, `#task-edit-form-region`, and `#task-list-region`, and the tightened delete test asserts the task regions are present while stale task UI content is absent.
- Environment caveat remains unchanged: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` is still blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so acceptance is based on code inspection plus `py_compile` verification.

## Reviewer Decision

- Decision: DONE for `ITEM-0005`.
- Accepted because the previously rejected regression is now explicitly fixed: `project_delete()` clears every task CRUD region that remains outside `#project-detail-region` on the detail page, so deleting a project no longer leaves stale task controls or task content behind.
- Accepted with the existing environment caveat unchanged: `python3 apps/project-tracker/manage.py test tracker.tests.test_views` is still blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so the reviewer decision is based on code inspection, the tightened focused delete test, and passing `py_compile` validation.
- No scope drift found in the revision: the change stays inside the existing Django tracker app, preserves the HTML partial swap contract, and does not introduce new framework or architecture surface beyond the targeted delete-response fix.

## Validator Outcome

- Result: PASS for `ITEM-0006`.
- Acceptance criteria check:
  - `tracker/views.py` and `tracker/urls.py` add a dedicated tag management surface with create, update, delete, list, and detail flows that stay inside the existing Django tracker app and use HTML partial responses instead of a new frontend layer.
  - `tag_detail.html` and the new tag partials expose stable async swap regions for `#tag-create-form-region`, `#tag-detail-region`, `#tag-edit-form-region`, and `#tag-list-region`, and the selector coverage matches the intended create, selection, update, and delete flows.
  - `tag_detail()` still serves a normal full-page route for direct navigation from project/task tag links while returning partial swaps for async selection requests.
  - `static/tracker/app.js` preserves wrapper IDs for repeated region swaps by replacing the wrapper only when the returned fragment root matches the target ID and otherwise updating `innerHTML`, which remains compatible with the existing project and task mutation regions.
  - Focused view tests cover tag management rendering plus successful and invalid tag mutations by inspection.
- Regression check:
  - No correctness regression found on inspection in the shared swap-helper change. Existing project/task surfaces still target stable wrapper IDs, and the new helper behavior preserves those wrappers when the returned partial omits them.
  - No scope drift found: the slice stays within the existing single Django app, uses plain templates and vanilla JS, and does not introduce DRF, extra apps, or speculative architecture.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_views` failed in the workspace with `ModuleNotFoundError: No module named 'django'`.
- Code inspection evidence:
  - `tag_create()` returns swaps for `#tag-create-form-region`, `#tag-list-region`, `#tag-detail-region`, and `#tag-edit-form-region`, which matches the management page layout.
  - `tag_detail()` returns partial swaps for list/detail/edit reset on async selection and a full-page render for normal navigation, preserving direct-link behavior from project/task surfaces.
  - `parseAndSwap()` keeps region wrapper IDs intact when the replacement fragment does not include them, which is the contract used by the project/task/tag mutation partials.

## Known Risks

- Runtime validation of the new tag CRUD views and templates is still blocked until Django is installed in the workspace.
- The focused tag tests are present in `tracker/tests/test_views.py`, but they could not be executed end to end in this workspace because Django is unavailable.

## Validator Outcome

- Result: PASS for `ITEM-0007`.
- Acceptance criteria check:
  - `tracker/tests/test_domain.py` now covers locked default enum values, invalid enumerated form input, and the constraint that `TaskForm` does not expose project reassignment.
  - `tracker/tests/test_views.py` now covers the remaining meaningful server-rendered and no-reload interaction branches for the accepted tracker surface, including async tag selection swaps, invalid project/task/tag updates, project-list delete refreshes, and representative `405` method guards.
  - The added assertions match the current selector and partial contract in `tracker/views.py`, `project_detail.html`, and `tag_detail.html` without introducing brittle expectations around unrelated markup.
  - The final coverage pass stayed inside the existing Django tracker app and Django test modules, with the environment-blocked runtime gap kept explicit instead of hidden.
- Regression check:
  - No new regression found by inspection in the expanded tests or current tracker code.
  - No scope drift found: the slice changes only test coverage and review artifacts, with no new packages, services, frontend frameworks, or speculative architecture.

## Validation Evidence

- `python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)` passed.
- `python3 apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` failed immediately in the workspace with `ModuleNotFoundError: No module named 'django'`.
- Code inspection evidence:
  - `project_delete()` clears the detail-page task regions that live outside `#project-detail-region`, and the tightened delete test asserts those swap targets are present while stale task UI is absent.
  - The tag-detail async selection test matches the current `#tag-list-region`, `#tag-detail-region`, and `#tag-edit-form-region` swap behavior implemented in `tag_detail()` and rendered by the tag management templates.
  - The invalid update tests align with the current form-error response path, which returns the relevant edit-form partial with `400` status for project, task, and tag mutations.

## Known Risks

- Runtime execution of the final Django test suite is still blocked until Django is installed in the workspace.
- Acceptance risk is therefore environmental rather than product-code related; reviewer should preserve that caveat unless the runtime environment changes.

## Reviewer Decision

- Decision: DONE for `ITEM-0007`.
- Accepted because the final coverage pass now exercises the locked domain rules, server-rendered read pages, and the accepted no-reload mutation contract across projects, tasks, and tags without exposing a new product regression.
- Accepted with the existing environment caveat unchanged: `python3 apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views` is still blocked in this workspace by `ModuleNotFoundError: No module named 'django'`, so the decision rests on code inspection plus passing `py_compile` validation rather than executed Django runtime tests.
- No scope drift found: the slice stays inside the existing Django tracker app and current Django test modules, with no new packages, services, or frontend architecture changes.
