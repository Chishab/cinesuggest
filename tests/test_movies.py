from app import db
from app.models.activity_log import ActivityLog
from app.models.movie import Movie


def seed_movies(app):
    with app.app_context():
        movies = [
            Movie(title="The Last Orbit", genre="Sci-Fi", description="A pilot explores a distant planet.", year=2023, rating=8.4, director="Ava Chen"),
            Movie(title="Midnight Signal", genre="Sci-Fi", description="An engineer follows a mysterious signal.", year=2022, rating=7.9, director="Noah Brooks"),
            Movie(title="Ocean Between Us", genre="Drama", description="Siblings restore a coastal lighthouse.", year=2023, rating=8.2, director="Leah Morgan"),
        ]
        db.session.add_all(movies)
        db.session.commit()
        return [movie.id for movie in movies]


def test_movie_search_and_genre_filter(client, app):
    seed_movies(app)

    response = client.get("/movies?q=Orbit&genre=Sci-Fi")

    assert response.status_code == 200
    assert b"The Last Orbit" in response.data
    assert b"Ocean Between Us" not in response.data


def test_movie_details_and_invalid_movie(client, app):
    movie_id = seed_movies(app)[0]

    response = client.get(f"/movie/{movie_id}")
    assert response.status_code == 200
    assert b"The Last Orbit" in response.data
    assert client.get("/movie/9999").status_code == 404


def test_recommendations_return_similar_movies(client, app):
    movie_id = seed_movies(app)[0]

    response = client.get(f"/recommend?movie_id={movie_id}")

    assert response.status_code == 200
    assert b"Because you liked The Last Orbit" in response.data
    assert b"Midnight Signal" in response.data
    assert b"The Last Orbit" not in response.data.split(b"Because you liked The Last Orbit", 1)[1]


def test_recommendation_success_and_invalid_id_are_logged(client, app):
    movie_id = seed_movies(app)[0]
    success_response = client.get(f"/recommend?movie_id={movie_id}")
    error_response = client.get("/recommend?movie_id=not-a-movie")

    assert success_response.status_code == 200
    assert error_response.status_code == 200
    assert b"Choose a valid movie" in error_response.data
    with app.app_context():
        events = db.session.scalars(
            db.select(ActivityLog).order_by(ActivityLog.id)
        ).all()
    assert [(event.event_type, event.outcome) for event in events] == [
        ("recommendation", "success"),
        ("recommendation", "error"),
    ]


def test_dashboard_shows_recent_activity(client):
    register_response = client.post(
        "/register",
        data={"username": "qa-user", "email": "qa@example.com", "password": "password123"},
    )
    dashboard_response = client.get("/dashboard")

    assert register_response.status_code == 302
    assert b"Recent activity" in dashboard_response.data
    assert b"A new account was registered" in dashboard_response.data
