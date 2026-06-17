# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Context

**Spendly** is a student learning project — a step-by-step scaffolded exercise to build a personal expense tracker web app. The tagline is "Track every rupee. Own your finances." Currency throughout the UI is Indian Rupees (₹).

The scaffold (routes, templates, CSS, JS wiring) is already provided. Students fill in backend logic step by step:

| Step | What to implement |
|---|---|
| 1 | `database/db.py` — `get_db`, `init_db`, `seed_db` |
| 2 | User registration (form handling + password hashing) |
| 3 | Login / logout with Flask sessions |
| 4 | Profile page |
| 7–9 | CRUD for expenses — add, edit, delete |

---

## Architecture

### Request Flow

```
Browser → app.py (route handler)
              ├── render_template("*.html")  →  templates/*.html extends base.html
              └── database/db.py (get_db)   →  SQLite file on disk
```

### Key Files

- `app.py` — single file containing all Flask routes; no blueprints
- `database/db.py` — SQLite helpers (placeholder; students implement this in Step 1)
- `templates/base.html` — master layout: navbar, footer, Google Fonts, global `<script>` tag; all pages extend it via `{% block content %}`
- `static/css/style.css` — all styles; uses CSS custom properties defined in `:root`
- `static/js/main.js` — global JS (currently empty; add interactivity here as features are built)

### Stub Routes (not yet implemented)

All live in `app.py` and currently return plain strings:

| Route | Step |
|---|---|
| `GET /logout` | Step 3 |
| `GET /profile` | Step 4 |
| `GET /expenses/add` | Step 7 |
| `GET /expenses/<int:id>/edit` | Step 8 |
| `GET /expenses/<int:id>/delete` | Step 9 |

### Database Layer Contract

`database/db.py` must export exactly three functions:
- `get_db()` — returns a `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — creates all tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — inserts sample rows for local development

---

## Code Style

**Python**
- PEP 8; 4-space indentation
- Route functions are named after the page they serve (e.g., `landing`, `login`, `register`)
- SQL queries go directly inside route functions or a dedicated helper; no ORM

**HTML / Jinja2**
- All templates start with `{% extends "base.html" %}` and fill `{% block content %}`
- Page-specific styles go in `{% block head %}` as an inline `<style>` tag (see `landing.html`)
- Page-specific scripts go in `{% block scripts %}` as an inline `<script>` tag (see `landing.html`)
- Use `{{ url_for('view_name') }}` for all internal links — never hard-code paths

**CSS**
- All design tokens (colors, fonts, radii, breakpoints) are CSS custom properties in `:root` inside `style.css` — never use raw hex/px values in new rules; reference a variable instead
- Utility button classes are `btn-primary`, `btn-ghost`, `btn-submit` — reuse them; do not add new button styles unless genuinely necessary
- Form inputs use the class `form-input`; labels use the class pattern `form-group > label + input`

**JavaScript**
- Vanilla JS only — no frameworks or build tools
- Wrap page-specific scripts in an IIFE `(function () { ... }())` to avoid polluting the global scope (see the video modal in `landing.html`)
- Lazy-load iframes by storing the real URL in `data-src` and copying to `src` only on open

---

## Preferred Libraries & Tools

| Purpose | Choice |
|---|---|
| Web framework | Flask 3.x |
| Database | SQLite (stdlib `sqlite3`) |
| Password hashing | `werkzeug.security` — `generate_password_hash` / `check_password_hash` |
| Sessions | Flask's built-in `session` (cookie-based) |
| Testing | `pytest` + `pytest-flask` |
| Fonts | Google Fonts — DM Sans (body) + DM Serif Display (headings) |

Do **not** introduce SQLAlchemy, an ORM, or any JS framework. The stack is intentionally minimal.

---

## Commands

### Setup

```bash
# Create and activate virtual environment (macOS system Python is externally managed — always use .venv)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
.venv/bin/python -m pip install -r requirements.txt
```

### Run the dev server

```bash
.venv/bin/python app.py
# → http://localhost:5001
```

### Run tests

```bash
# All tests
.venv/bin/python -m pytest

# Single test file
.venv/bin/python -m pytest tests/test_auth.py

# Single test function
.venv/bin/python -m pytest tests/test_auth.py::test_login

# Verbose output
.venv/bin/python -m pytest -v
```

### Add a dependency

```bash
.venv/bin/python -m pip install <package>
# Then pin it:
.venv/bin/python -m pip freeze | grep <package> >> requirements.txt
```

---

## Critical Rules

1. **Never use the system Python.** macOS marks `/opt/homebrew/bin/python3` as externally managed. Always prefix commands with `.venv/bin/python` or activate `.venv` first.
2. **All new routes must use `url_for`** in templates — never hard-code URLs like `/login`.
3. **Hash passwords with `werkzeug.security`** — never store or compare plain-text passwords.
4. **Enable foreign keys** every time you open a SQLite connection: `PRAGMA foreign_keys = ON`.
5. **All templates must extend `base.html`** — do not write standalone HTML files.
6. **Pin new dependencies** in `requirements.txt` immediately after installing.

---

## Warnings, Edge Cases & Things to Avoid

- **`pip` / `python` not on PATH** — on macOS, `pip` and `python` commands are often missing or point to the system-managed interpreter. Always use `.venv/bin/python -m pip`.
- **Session secret key** — Flask sessions are unsigned without `app.secret_key`. Set it before implementing auth (`app.secret_key = os.urandom(24)` in dev, an env var in prod).
- **SQLite `row_factory`** — without `conn.row_factory = sqlite3.Row`, cursor rows are plain tuples; Jinja2 templates will break when accessing columns by name.
- **CSRF** — the login/register forms have no CSRF token yet. Do not add production-facing auth without adding protection (e.g., `Flask-WTF`).
- **Do not use Blueprints** unless explicitly required — the project deliberately keeps everything in `app.py` for simplicity.
- **Do not add page-specific CSS to `style.css`** — keep page-scoped styles in the template's `{% block head %}` to avoid polluting the global stylesheet.
- **`data-src` iframe pattern** — the video modal lazy-loads its iframe by storing the URL in `data-src` and only copying it to `src` on open. If you touch the modal, preserve this pattern to avoid auto-playing the video on page load.
- **Responsive breakpoints** — the CSS has two breakpoints: `900px` (collapse feature grid) and `600px` (hide nav links, stack stats). Test new layout sections at both widths.
