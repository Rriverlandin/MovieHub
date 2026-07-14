"""
seed.py — populate MovieHub with a demo account and a generous movie list.

Usage:
    python seed.py

Creates (if not already present) a user:
    username: demo
    password: demo1234

...and fills their collection with ~30 movies across genres, with a mix
of watched/unwatched and favorite/non-favorite so the dashboard looks
alive right away. Safe to run multiple times — it won't duplicate the
demo user, and only adds movies the demo user doesn't already have.
"""

from werkzeug.security import generate_password_hash

from app import create_app
from models import db, User, Movie

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"

MOVIES = [
    {"title": "Inception", "year": 2010, "genre": "Sci-Fi", "rating": 9, "poster": "🌀", "watched": True, "favorite": True},
    {"title": "Parasite", "year": 2019, "genre": "Thriller", "rating": 9, "poster": "🏚️", "watched": True, "favorite": True},
    {"title": "Whiplash", "year": 2014, "genre": "Drama", "rating": 8, "poster": "🥁", "watched": True, "favorite": False},
    {"title": "Dune", "year": 2021, "genre": "Sci-Fi", "rating": 8, "poster": "🏜️", "watched": False, "favorite": False},
    {"title": "Amélie", "year": 2001, "genre": "Romance", "rating": 8, "poster": "🍒", "watched": True, "favorite": True},
    {"title": "Mad Max: Fury Road", "year": 2015, "genre": "Action", "rating": 9, "poster": "🚀", "watched": True, "favorite": True},
    {"title": "The Grand Budapest Hotel", "year": 2014, "genre": "Comedy", "rating": 8, "poster": "🎭", "watched": True, "favorite": False},
    {"title": "Get Out", "year": 2017, "genre": "Horror", "rating": 8, "poster": "👻", "watched": True, "favorite": False},
    {"title": "John Wick", "year": 2014, "genre": "Action", "rating": 7, "poster": "🔫", "watched": True, "favorite": False},
    {"title": "La La Land", "year": 2016, "genre": "Musical", "rating": 7, "poster": "💔", "watched": True, "favorite": False},
    {"title": "Spirited Away", "year": 2001, "genre": "Animation", "rating": 10, "poster": "🎬", "watched": True, "favorite": True},
    {"title": "The Dark Knight", "year": 2008, "genre": "Action", "rating": 10, "poster": "🦇", "watched": True, "favorite": True},
    {"title": "Interstellar", "year": 2014, "genre": "Sci-Fi", "rating": 9, "poster": "🌌", "watched": True, "favorite": True},
    {"title": "Everything Everywhere All at Once", "year": 2022, "genre": "Sci-Fi", "rating": 9, "poster": "🥯", "watched": True, "favorite": True},
    {"title": "The Shawshank Redemption", "year": 1994, "genre": "Drama", "rating": 10, "poster": "🔑", "watched": True, "favorite": True},
    {"title": "Knives Out", "year": 2019, "genre": "Mystery", "rating": 8, "poster": "🔪", "watched": True, "favorite": False},
    {"title": "Oppenheimer", "year": 2023, "genre": "Drama", "rating": 9, "poster": "💣", "watched": False, "favorite": False},
    {"title": "The Batman", "year": 2022, "genre": "Action", "rating": 7, "poster": "🌧️", "watched": False, "favorite": False},
    {"title": "Coco", "year": 2017, "genre": "Animation", "rating": 9, "poster": "💀", "watched": True, "favorite": True},
    {"title": "Blade Runner 2049", "year": 2017, "genre": "Sci-Fi", "rating": 8, "poster": "🌆", "watched": False, "favorite": False},
    {"title": "The Social Network", "year": 2010, "genre": "Drama", "rating": 7, "poster": "💻", "watched": True, "favorite": False},
    {"title": "Your Name", "year": 2016, "genre": "Animation", "rating": 9, "poster": "🌠", "watched": True, "favorite": True},
    {"title": "Gone Girl", "year": 2014, "genre": "Thriller", "rating": 8, "poster": "📓", "watched": True, "favorite": False},
    {"title": "The Grand Tour", "year": 2019, "genre": "Adventure", "rating": 6, "poster": "🚗", "watched": False, "favorite": False},
    {"title": "Portrait of a Lady on Fire", "year": 2019, "genre": "Romance", "rating": 9, "poster": "🔥", "watched": True, "favorite": True},
    {"title": "Django Unchained", "year": 2012, "genre": "Western", "rating": 8, "poster": "🐎", "watched": True, "favorite": False},
    {"title": "Arrival", "year": 2016, "genre": "Sci-Fi", "rating": 8, "poster": "🛸", "watched": False, "favorite": False},
    {"title": "The Matrix", "year": 1999, "genre": "Sci-Fi", "rating": 9, "poster": "💊", "watched": True, "favorite": True},
    {"title": "Pan's Labyrinth", "year": 2006, "genre": "Fantasy", "rating": 8, "poster": "🌿", "watched": False, "favorite": False},
    {"title": "Soul", "year": 2020, "genre": "Animation", "rating": 8, "poster": "🎹", "watched": True, "favorite": False},
]


def seed():
    app = create_app()

    with app.app_context():
        user = User.query.filter_by(username=DEMO_USERNAME).first()

        if user is None:
            user = User(
                username=DEMO_USERNAME,
                password=generate_password_hash(DEMO_PASSWORD),
            )
            db.session.add(user)
            db.session.commit()
            print(f"Created demo user: {DEMO_USERNAME} / {DEMO_PASSWORD}")
        else:
            print(f"Demo user already exists: {DEMO_USERNAME}")

        existing_titles = {m.title for m in user.movies}
        added = 0

        for entry in MOVIES:
            if entry["title"] in existing_titles:
                continue
            db.session.add(Movie(user_id=user.id, **entry))
            added += 1

        db.session.commit()
        print(f"Added {added} new movies. {DEMO_USERNAME} now has {len(user.movies)} total.")


if __name__ == "__main__":
    seed()
