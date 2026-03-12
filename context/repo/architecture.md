# Project Tracker Architecture

## Chosen approach

Build a single Django project under `apps/project-tracker/` with one primary Django app for the product domain. Use server-rendered templates as the default UI surface and small asynchronous interactions for create, edit, and delete flows so the page does not fully reload.

## Proposed structure

- `apps/project-tracker/manage.py`
- `apps/project-tracker/project_tracker/`
  - `settings.py`, `urls.py`, `asgi.py`, `wsgi.py`
- `apps/project-tracker/tracker/`
  - `models.py`
  - `forms.py`
  - `views.py`
  - `urls.py`
  - `admin.py`
  - `tests/`
- `apps/project-tracker/templates/tracker/`
  - `base.html`
  - `dashboard.html`
  - `project_list.html`
  - `project_detail.html`
  - `tag_detail.html`
  - `partials/`
- `apps/project-tracker/static/tracker/`
  - `app.css`
  - `app.js`

## Domain boundaries

- `Project`: name, description, status, created_date, tags.
- `Task`: project, title, status, priority, due_date, tags.
- `Tag`: label/name shared by projects and tasks through many-to-many relations.

Keep business rules near models and forms. Avoid service layers unless repeated logic becomes concrete.

## View and endpoint strategy

- Full-page GET views:
  - dashboard summary
  - project list
  - project detail with related tasks
  - tag filter/detail view
- Mutation endpoints:
  - create, update, delete for projects
  - create, update, delete for tasks
  - create, update, delete for tags

Each mutation should return either:

- an HTML partial for the updated list/detail region, or
- a small JSON envelope only when the client needs minimal status data to drive a targeted DOM update.

Default to HTML partial responses because they keep rendering rules on the server and reduce duplicated template logic in JavaScript.

## Frontend interaction model

Use vanilla JavaScript with event delegation and `fetch` for form submissions and destructive actions. Mark asynchronously enhanced forms and buttons with explicit data attributes. The server remains the source of truth for rendered markup; JavaScript only swaps returned fragments into the DOM and handles lightweight error display.

## Data and querying

- SQLite is the only persistence layer.
- Use straightforward Django ORM queries.
- Dashboard counts should be direct aggregate queries:
  - total projects
  - tasks by status
  - overdue tasks where due_date is before today and status is not `done`

Do not add caching, background jobs, or analytics infrastructure.

## Tradeoffs

- One Django app is preferred over multiple apps because the domain is small and tightly related.
- HTML partials are preferred over a broad JSON API because the product is server-rendered and CRUD-focused.
- Forms provide validation and error rendering with less custom code than handwritten request parsing.
- Keep URLs explicit instead of introducing generic viewsets or abstraction-heavy CRUD helpers.

## Risks to watch

- No-reload CRUD can become inconsistent if some mutations return JSON and others return HTML without a clear rule. Keep partial HTML as the default.
- Tag management touches both projects and tasks, so form handling and partial refresh boundaries should stay explicit.
- SQLite is sufficient here, but tests and code should avoid assumptions about concurrent writes or advanced database features.
