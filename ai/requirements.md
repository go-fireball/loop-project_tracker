# Requirements (One Pager)

## Objective

Build a personal project tracker web app: a Django-based application backed by SQLite that lets a user manage projects, tasks, and tags through a plain HTML/CSS/JS frontend. Django serves both the JSON API and HTML templates from a single project under `apps/project-tracker/`.

## In Scope

- **Projects** — create, read, update, delete. Each project has: name, description, status (`active` / `completed` / `archived`), and created date.
- **Tasks** — create, read, update, delete. Each task belongs to exactly one project and has: title, status (`todo` / `in_progress` / `done`), priority (`low` / `medium` / `high`), and due date.
- **Tags** — create, read, update, delete. Tags are assignable to both projects and tasks (many-to-many).
- **API** — Django views (no DRF) returning JSON for all CRUD operations on the three entities.
- **Frontend views** (served as Django templates):
  - Projects list view
  - Project detail view (shows the project and its tasks)
  - Tag filter view (filter projects/tasks by tag)
  - Dashboard view (summary stats: total projects, tasks by status, overdue tasks)
- **Async interactions** — add, edit, and delete operations must work without a full page reload (vanilla JS fetch calls to the JSON API).
- **Persistence** — all data stored in SQLite via Django ORM.

## Out of Scope

- Governance loop internals (already bootstrapped)
- User authentication / multi-user support
- External database servers (Postgres, MySQL, etc.)
- Frontend JS frameworks (React, Vue, Angular, etc.)
- Additional pip packages beyond Django and its built-in dependencies (no DRF, Celery, etc.)
- Microservices or separate backend services
- File/image attachments
- Email or notification features

## Constraints

- Django with built-in dependencies only — no third-party pip packages
- No frontend JS frameworks — plain HTML, CSS, and vanilla JS only
- Single Django project — no microservices
- SQLite only — no external database server
- All code lives in `apps/project-tracker/`
- Django serves both the API (JSON) and static/template files

## Acceptance Criteria

1. A project can be created, listed, viewed, edited, and deleted via the UI without a full page reload for mutations.
2. A task can be created (linked to a project), listed within its project, edited, and deleted without a full page reload for mutations.
3. A tag can be created and attached to or detached from a project or task without a full page reload.
4. The tag filter view shows projects and/or tasks filtered by a selected tag.
5. The dashboard displays: total project count, task counts by status (`todo`, `in_progress`, `done`), and a count of overdue tasks (due date in the past, status not `done`).
6. All data survives a server restart (SQLite persistence).
7. The app runs with `python manage.py runserver` after `python manage.py migrate` — no extra setup steps.

## Open Questions

- None — requirements are fully derivable from the stated goal.
