# Spec: Login and Logout

## Overview
This step wires up session-based authentication so users can sign in and sign out of Spendly. The `GET /login` route already renders the form; this step adds the `POST /login` handler that looks up the user by email, verifies the password with `werkzeug.security.check_password_hash`, stores `user_id` and `user_name` in Flask's signed cookie session, and redirects to the profile page on success. The `GET /logout` stub is also replaced: it clears the session and redirects to the landing page. The navbar in `base.html` is made session-aware — logged-in users see "Profile" and "Sign out"; guests see "Sign in" and "Get started". After this step, only authenticated users should be able to reach protected pages.

## Depends on
- **Step 1 — Database Setup**: `get_db()` and the `users` table must exist.
- **Step 2 — Registration**: At least one real user must be creatable (or the seeded demo user used) to verify login works end-to-end.

## Routes
- `POST /login` — process login form; verify credentials; set session; redirect to `/profile` on success — public
- `GET /logout` — clear session; redirect to `/` — logged-in only (but safe to hit when already logged out)

## Database changes
No database changes. The `users` table already has `id`, `email`, and `password_hash`, which are the only columns needed for authentication.

## Templates
- **Modify:** `templates/login.html`
  - Change `action="/login"` → `action="{{ url_for('login') }}"` (remove hardcoded path)
  - Add `value="{{ email or '' }}"` to the email input so it is re-populated on a failed login attempt
- **Modify:** `templates/base.html`
  - Update the `<div class="nav-links">` block to be session-aware:
    - When `session.user_id` is set: show a "Profile" link (`url_for('profile')`) and a "Sign out" link (`url_for('logout')`)
    - When no session: keep existing "Sign in" and "Get started" links

## Files to change
- `app.py`
  - Add `session` to the Flask import line (already imports `redirect`, `url_for`, `request`)
  - Add `check_password_hash` to the `werkzeug.security` import
  - Convert `login` route to handle both `GET` and `POST` (`methods=["GET", "POST"]`)
    - On `POST`: look up user by email; call `check_password_hash`; on match set `session['user_id']` and `session['user_name']`; redirect to `url_for('profile')`; on failure re-render `login.html` with `error` and pre-filled `email`
  - Replace the `logout` stub with a real implementation: call `session.clear()`, then redirect to `url_for('landing')`
- `templates/login.html`
  - Fix hardcoded `action="/login"` → `action="{{ url_for('login') }}"`
  - Add `value="{{ email or '' }}"` to the email input
- `templates/base.html`
  - Make `nav-links` conditional on `session.get('user_id')`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (which provides `check_password_hash`) is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security` — use `check_password_hash` to verify; never compare plain text
- Use `session.clear()` for logout — do not manually delete individual keys
- Use CSS variables — never hardcode hex values in any new markup
- All templates extend `base.html`
- Use `url_for` for all redirects and form actions — never hardcode paths
- Do not add a `@login_required` decorator or any custom decorator — keep everything inline in `app.py` for now

## Definition of done
- [ ] Submitting valid credentials (`demo@spendly.com` / `demo123`) signs the user in and redirects to `/profile`
- [ ] After login, `session['user_id']` and `session['user_name']` are set
- [ ] Submitting an unknown email re-renders the login form with an error message and the email pre-filled
- [ ] Submitting a correct email but wrong password re-renders the login form with a generic error (do not reveal which field was wrong)
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] After logout, `session` contains no `user_id`
- [ ] The navbar shows "Profile" and "Sign out" when logged in, and "Sign in" / "Get started" when logged out
- [ ] The login form's `action` attribute uses `url_for('login')`, not a hardcoded path
- [ ] Visiting `/login` when already logged in still renders the form (no redirect loop)
