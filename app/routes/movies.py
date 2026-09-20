from flask import Blueprint, abort, render_template, request
from sqlalchemy import or_

from app import db
from app.models.movie import Movie

movies_bp = Blueprint("movies", __name__)


@movies_bp.get("/movies")
def movies():
    query = request.args.get("q", "").strip()
    genre = request.args.get("genre", "").strip()
    sort = request.args.get("sort", "title")

    statement = db.select(Movie)
    if query:
        search = f"%{query}%"
        statement = statement.where(
            or_(Movie.title.ilike(search), Movie.description.ilike(search))
        )
    if genre:
        statement = statement.where(Movie.genre == genre)
    if sort == "rating":
        statement = statement.order_by(Movie.rating.desc(), Movie.title.asc())
    elif sort == "year":
        statement = statement.order_by(Movie.year.desc(), Movie.title.asc())
    else:
        statement = statement.order_by(Movie.title.asc())

    movie_list = db.session.scalars(statement).all()
    genres = db.session.scalars(db.select(Movie.genre).distinct().order_by(Movie.genre)).all()
    return render_template(
        "movies.html", movies=movie_list, genres=genres, query=query, genre=genre, sort=sort
    )


@movies_bp.get("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    return render_template("movie_details.html", movie=movie)
