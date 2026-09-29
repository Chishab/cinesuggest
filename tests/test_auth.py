from app import db
from app.models.activity_log import ActivityLog
from app.models.user import User


def register(client, username="ada", email="ada@example.com", password="password123"):
    return client.post(
        "/register",
        data={"username": username, "email": email, "password": password},
        follow_redirects=True,
    )


def login(client, email="ada@example.com", password="password123"):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_database_initializes_and_registration_hashes_password(client, app):
    response = register(client)

    assert response.status_code == 200
    assert b"Registration successful" in response.data
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.email == "ada@example.com"))
        assert user is not None
        assert user.password_hash != "password123"
        assert user.check_password("password123")


def test_registration_validates_required_fields(client):
    response = client.post(
        "/register", data={"username": "", "email": "bad", "password": "short"}
    )

    assert response.status_code == 200
    assert b"required" in response.data


def test_duplicate_registration_is_rejected(client):
    register(client)
    response = register(client, username="another", email="ada@example.com")

    assert response.status_code == 200
    assert b"already registered" in response.data


def test_login_and_logout_manage_session(client):
    register(client)
    response = login(client)

    assert response.status_code == 200
    assert b"Welcome back, ada" in response.data
    with client.session_transaction() as session:
        assert session["username"] == "ada"

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"logged out" in response.data
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_invalid_login_is_rejected(client):
    register(client)
    response = login(client, password="wrong-password")

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_auth_events_are_logged_without_credentials(client, app):
    register(client, username="private-user", email="private@example.com")
    login(client, email="private@example.com", password="wrong-password")
    login(client, email="private@example.com")

    with app.app_context():
        events = db.session.scalars(
            db.select(ActivityLog).order_by(ActivityLog.id)
        ).all()
        event_data = " ".join(event.message for event in events)

    assert [(event.event_type, event.outcome) for event in events] == [
        ("registration", "success"),
        ("login", "error"),
        ("login", "success"),
    ]
    assert "private@example.com" not in event_data
    assert "wrong-password" not in event_data
    assert "password123" not in event_data


def test_registration_errors_are_logged(client, app):
    client.post(
        "/register",
        data={"username": "", "email": "bad-email", "password": "short"},
    )
    register(client)
    register(client, username="another", email="ada@example.com")

    with app.app_context():
        events = db.session.scalars(
            db.select(ActivityLog).where(ActivityLog.event_type == "registration")
        ).all()

    assert [(event.outcome, event.message) for event in events] == [
        ("error", "Registration rejected: required fields missing"),
        ("success", "A new account was registered"),
        ("error", "Registration rejected: account already exists"),
    ]
