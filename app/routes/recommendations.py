from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models.movie import Movie
from app.services.activity import record_activity
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
            movie_id = int(selected_id)
        except (TypeError, ValueError):
            movie_id = None

        selected_movie = db.session.get(Movie, movie_id) if movie_id is not None else None
        if selected_movie is None:
            record_activity("recommendation", "error", "Recommendation failed: selected movie was not found")
            flash("Choose a valid movie to get recommendations.", "danger")
        else:
            results = recommend_movies(selected_movie, movies)
            if results:
                record_activity(
                    "recommendation",
                    "success",
                    f"Generated {len(results)} recommendations for {selected_movie.title}",
                )
            else:
                record_activity(
                    "recommendation", "error", "Recommendation failed: no results available"
                )
                flash("No recommendations are available for this movie yet.", "warning")

    return render_template(
        "recommendations.html",
        movies=movies,
        selected_movie=selected_movie,
        recommendations=results,
        selected_id=selected_id,
    )
