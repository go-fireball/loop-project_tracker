# Project Tracker

Personal project tracker built with Django, SQLite, server-rendered templates, and vanilla JavaScript.

## Local setup

Run everything from the repository root unless a command says otherwise.

### 1. Install the locked Python version with pyenv

```bash
pyenv install 3.12
pyenv local 3.12
```

The repository is locked to Python 3.12+ in `pyproject.toml`. If your local `pyenv` already has a compatible 3.12.x version installed, reuse that version instead of reinstalling it.

### 2. Install dependencies with Poetry

```bash
poetry install
```

This project is locked to Django plus built-in dependencies only. The repository root `pyproject.toml` currently declares Python `^3.12` and Django `^5.1`.

### 3. Apply migrations

```bash
poetry run python apps/project-tracker/manage.py migrate
```

This uses the SQLite database at `apps/project-tracker/db.sqlite3`.

### 4. Run the development server

```bash
poetry run python apps/project-tracker/manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Focused verification

### Python compile check

```bash
python3 -m py_compile $(find apps/project-tracker -name '*.py' | sort)
```

### Focused Django tests

```bash
poetry run python apps/project-tracker/manage.py test tracker.tests.test_domain tracker.tests.test_views
```

## Environment caveat

If Django is not yet installed in the active Poetry environment, Django runtime commands fail with:

```text
ModuleNotFoundError: No module named 'django'
```

Treat that as a local setup problem, not as a defect in the tracker application. Once `poetry install` has completed successfully, the migration, `runserver`, and focused test commands above are the expected verification path.

## Stack

- Backend: Django only
- Database: SQLite
- Frontend: server-rendered HTML, CSS, and vanilla JS
