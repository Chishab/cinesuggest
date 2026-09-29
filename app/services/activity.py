from app import db
from app.models.activity_log import ActivityLog


def record_activity(event_type, outcome, message):
    db.session.add(
        ActivityLog(event_type=event_type, outcome=outcome, message=message)
    )
    db.session.commit()
