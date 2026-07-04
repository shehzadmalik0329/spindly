import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.urandom(24)


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html",
                               error="All fields are required.",
                               name=name, email=email)

    if len(password) < 8:
        return render_template("register.html",
                               error="Password must be at least 8 characters.",
                               name=name, email=email)

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template("register.html",
                               error="An account with that email already exists.",
                               name=name, email=email)
    finally:
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?",
        (email,),
    ).fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html",
                               error="Invalid email or password.",
                               email=email)

    session.clear()
    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms-and-conditions.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "member_since": "June 2025",
        "initials": "RS",
    }
    stats = {
        "total_spent": "3,799.00",
        "transaction_count": 8,
        "top_category": "Bills",
    }
    expenses = [
        {"date": "Jun 16", "description": "Dinner with friends",  "category": "Food",          "amount": "180.00"},
        {"date": "Jun 14", "description": "Stationery",           "category": "Other",         "amount": "200.00"},
        {"date": "Jun 12", "description": "Clothes",              "category": "Shopping",      "amount": "850.00"},
        {"date": "Jun 10", "description": "OTT subscription",     "category": "Entertainment", "amount": "399.00"},
        {"date": "Jun 08", "description": "Pharmacy",             "category": "Health",        "amount": "500.00"},
    ]
    categories = [
        {"name": "Bills",         "amount": "1,200.00", "pct": 32},
        {"name": "Shopping",      "amount": "850.00",   "pct": 22},
        {"name": "Health",        "amount": "500.00",   "pct": 13},
        {"name": "Food",          "amount": "500.00",   "pct": 13},
        {"name": "Entertainment", "amount": "399.00",   "pct": 11},
        {"name": "Other",         "amount": "200.00",   "pct": 5},
        {"name": "Transport",     "amount": "150.00",   "pct": 4},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           expenses=expenses, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
