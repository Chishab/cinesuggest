from app import db
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
