import csv
from pathlib import Path

from app import create_app, db
from app.models.movie import Movie


app = create_app()
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "movies.csv"

with app.app_context():
    inserted = 0
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if db.session.scalar(db.select(Movie).where(Movie.title == row["title"])):
                continue
            db.session.add(
                Movie(
                    title=row["title"],
                    genre=row["genre"],
                    description=row["description"],
                    year=int(row["year"]),
                    rating=float(row["rating"]),
                    director=row["director"],
                    poster_url=row["poster_url"] or None,
                )
            )
            inserted += 1
    db.session.commit()
    print(f"Inserted {inserted} movies from {DATA_FILE}")
