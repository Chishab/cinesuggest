from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("home.html", username=session.get("username"))


@main_bp.get("/home")
def home():
    return render_template("home.html", username=session.get("username"))
