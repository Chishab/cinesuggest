from flask import Blueprint, redirect, render_template, url_for

from app import db
from app.models.activity_log import ActivityLog
from app.services.qa_metrics import build_metrics


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/qa-dashboard")
def dashboard_alias():
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.get("/dashboard")
def dashboard():
    activity_logs = db.session.scalars(
        db.select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(50)
    ).all()
    return render_template(
        "dashboard.html", metrics=build_metrics(), activity_logs=activity_logs
    )
