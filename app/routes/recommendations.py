from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.movie import Movie
from app.services.recommender import recommend_movies

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.get("/recommendations")
def recommendations_alias():
    return redirect(url_for("recommendations.recommend"))


@recommendations_bp.route("/recommend", methods=["GET", "POST"])
def recommend():
    movies = db.session.scalars(db.select(Movie).order_by(Movie.title)).all()
    selected_movie = None
    results = []
    selected_id = request.values.get("movie_id", "")

    if selected_id:
        try:
            selected_movie = db.get_or_404(Movie, int(selected_id))
            results = recommend_movies(selected_movie, movies)
        except (TypeError, ValueError):
            selected_movie = None

    return render_template(
        "recommendations.html",
        movies=movies,
        selected_movie=selected_movie,
        recommendations=results,
        selected_id=selected_id,
    )
