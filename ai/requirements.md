# Requirements (One Pager)

## Objective

Build a personal project tracker web app in Django that lets a single user manage projects, tasks, and tags through a server-rendered HTML/JavaScript frontend backed by a SQLite database. The product must support fast CRUD workflows without full page reloads and provide a dashboard summarizing project and task status.

## In Scope

- Django models for projects, tasks, and tags with the relationships defined in `ai/goal.yaml`
- HTTP endpoints for create, read, update, and delete operations on projects, tasks, and tags
- Project list view, project detail view with related tasks, tag filter view, and dashboard summary view
- Plain HTML, CSS, and vanilla JavaScript frontend served by Django
- Partial page updates or asynchronous requests so add/edit/delete flows do not require full page reloads
- SQLite-backed persistence for all project data

## Out of Scope

- Governance loop internals (already bootstrapped)
- Multi-user accounts, authentication, or permissions
- External APIs, background jobs, or real-time collaboration
- Frontend frameworks or third-party Django extensions

## Constraints

- Use Django and built-in dependencies only; do not add packages such as Django REST Framework
- Use SQLite as the only database
- Use plain HTML, CSS, and vanilla JavaScript; no React, Vue, or Angular
- Keep the solution as a single Django project
- Place implementation code under `apps/project-tracker/`

## Acceptance Criteria

- Projects support CRUD and include `name`, `description`, `status` (`active`, `completed`, `archived`), and `created_date`
- Tasks support CRUD, belong to a project, and include `title`, `status` (`todo`, `in_progress`, `done`), `priority` (`low`, `medium`, `high`), and `due_date`
- Tags support CRUD and can be associated many-to-many with both projects and tasks
- The frontend exposes separate views for a projects list, a single project detail page showing tasks, and a tag-based filter view
- Create, edit, and delete interactions for projects, tasks, and tags complete without a full page reload
- A dashboard shows total project count, task counts by status, and overdue task count
- Data persists across application restarts using SQLite
