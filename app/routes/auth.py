import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import or_

from app import db
from app.models.user import User
from app.services.activity import record_activity

auth_bp = Blueprint("auth", __name__)


def valid_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            record_activity("registration", "error", "Registration rejected: required fields missing")
            flash("Username, email, and password are required.", "danger")
        elif len(password) < 8:
            record_activity("registration", "error", "Registration rejected: password is too short")
            flash("Password must be at least 8 characters long.", "danger")
        elif not valid_email(email):
            record_activity("registration", "error", "Registration rejected: invalid email format")
            flash("Enter a valid email address.", "danger")
        elif db.session.scalar(
            db.select(User).where(or_(User.username == username, User.email == email))
        ):
            record_activity("registration", "error", "Registration rejected: account already exists")
            flash("Username or email is already registered.", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            record_activity("registration", "success", "A new account was registered")
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db.session.scalar(db.select(User).where(User.email == email))

        if user is None or not user.check_password(password):
            record_activity("login", "error", "Login rejected: invalid credentials")
            flash("Invalid email or password.", "danger")
        else:
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            record_activity("login", "success", "A user logged in successfully")
            flash(f"Welcome back, {user.username}.", "success")
            return redirect(url_for("main.home"))

    return render_template("login.html")


@auth_bp.get("/logout")
def logout():
    record_activity("logout", "success", "A user logged out")
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
