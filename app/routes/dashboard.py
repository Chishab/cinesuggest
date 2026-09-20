from flask import Blueprint, redirect, render_template, url_for

from app.services.qa_metrics import build_metrics


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/qa-dashboard")
def dashboard_alias():
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html", metrics=build_metrics())
