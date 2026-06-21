# Spec: Registration

## Overview
This step wires up the user registration form so new users can create an account. The `GET /register` route already renders the form; this step adds the `POST /register` handler that validates the submitted data, hashes the password using `werkzeug.security`, inserts a new row into the `users` table, shows the success message and redirects to the login page on success. Duplicate-email errors are caught and re-rendered on the form with a human-readable message. After this step, real users (not just the seeded demo account) can sign up for Spendly.

## Depends on
- **Step 1 — Database Setup**: `get_db()`, `init_db()`, and the `users` table must exist.

## Routes
- `POST /register` — process registration form; insert user; redirect to `/login` on success — public

## Database changes
No database changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) was created in Step 1.

## Templates
- **Modify:** `templates/register.html`
  - Change `action="/register"` → `action="{{ url_for('register') }}"` to remove the hardcoded path
  - No other markup changes needed (the `{% if error %}` block is already present)

## Files to change
- `app.py`
  - Add `request`, `redirect` to the Flask import line
  - Convert the `register` route to handle both `GET` and `POST` (`methods=["GET", "POST"]`)
  - On `POST`: validate inputs, check for duplicate email, hash password, insert user, redirect to `url_for('login')`
  - On validation/duplicate error: re-render `register.html` with an `error` string and the previously entered `name` and `email` so the user does not have to retype them
- `templates/register.html`
  - Fix hardcoded `action="/register"` → `action="{{ url_for('register') }}"`
  - Pass `value="{{ name or '' }}"` and `value="{{ email or '' }}"` to the name and email inputs so they are re-populated on error

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Hash passwords with `werkzeug.security.generate_password_hash`; never store plain text
- Catch duplicate-email violations via `sqlite3.IntegrityError` and surface a friendly error message
- Validate server-side: `name`, `email`, and `password` must all be non-empty; `password` must be at least 8 characters
- Use CSS variables — never hardcode hex values in any new markup
- All templates extend `base.html`
- Use `url_for` for all redirects and form actions — never hardcode paths

## Definition of done
- [ ] Submitting the form with valid, unique details creates a new row in `users` with a hashed password (not plain text)
- [ ] After successful registration the browser is redirected to `/login`
- [ ] Submitting with a duplicate email re-renders the form with an error message and the user's name and email pre-filled
- [ ] Submitting with an empty field re-renders the form with an error (server-side check, not just browser `required`)
- [ ] Submitting with a password shorter than 8 characters re-renders the form with an error
- [ ] The demo user created by `seed_db()` is unaffected and can still log in as `demo@spendly.com`
- [ ] The form's `action` attribute uses `url_for('register')`, not a hardcoded path
- [ ] No plain-text password appears anywhere in the database or logs
