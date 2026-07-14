from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utcnow() -> datetime:
    """Timezone-aware UTC timestamp helper (avoids naive datetimes)."""
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password = db.Column(
        db.String(255),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow,
        nullable=False,
    )

    movies = db.relationship(
        "Movie",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Movie.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"

    # ---- convenience stats, so templates stay dumb ----
    @property
    def total_movies(self) -> int:
        return len(self.movies)

    @property
    def watched_count(self) -> int:
        return sum(1 for m in self.movies if m.watched)

    @property
    def favorite_count(self) -> int:
        return sum(1 for m in self.movies if m.favorite)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    genre = db.Column(
        db.String(50),
    )

    year = db.Column(
        db.Integer,
    )

    rating = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    favorite = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    watched = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    poster = db.Column(
        db.String(500),
    )

    review = db.Column(
        db.Text,
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        db.CheckConstraint("rating >= 0 AND rating <= 10", name="ck_movie_rating_range"),
    )

    def __repr__(self) -> str:
        return f"<Movie id={self.id} title={self.title!r} user_id={self.user_id}>"

    def apply_form(self, form) -> None:
        """Update fields from a submitted form dict. Shared by add/edit routes."""
        self.title = form.get("title", self.title).strip()
        self.genre = (form.get("genre") or "").strip() or None
        self.poster = (form.get("poster") or "").strip() or None

        year = form.get("year")
        self.year = int(year) if year and year.isdigit() else self.year

        rating = form.get("rating")
        if rating and rating.isdigit():
            self.rating = max(0, min(10, int(rating)))

        self.favorite = bool(form.get("favorite"))
        self.watched = bool(form.get("watched"))
