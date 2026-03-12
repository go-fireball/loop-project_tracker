# Project Tracker

A personal project tracker web app built with Django, SQLite, and vanilla HTML/CSS/JS.

## Features

- CRUD operations on **projects**, **tasks**, and **tags**
- Dashboard with summary stats (total projects, tasks by status, overdue tasks)
- Project detail view showing associated tasks
- Tag management surface with many-to-many relationships to projects and tasks
- All create/edit/delete operations work without full page reloads (HTML partial swap pattern)

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)

## Setup

From the **repository root**:

```bash
poetry install
```

This installs Django and all dependencies into an isolated virtual environment managed by Poetry.

## Apply migrations

```bash
cd apps/project-tracker
poetry run python manage.py migrate
```

The database is SQLite at `apps/project-tracker/db.sqlite3`.

## Run the development server

```bash
cd apps/project-tracker
poetry run python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Run tests

```bash
cd apps/project-tracker
poetry run python manage.py test tracker
```

For verbose output:

```bash
poetry run python manage.py test tracker --verbosity=2
```

## Static syntax check

```bash
python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)
```

## Stack

- **Backend:** Django (no DRF, no extra packages)
- **Database:** SQLite
- **Frontend:** Server-rendered Django templates, vanilla JS
- **Package manager:** Poetry
