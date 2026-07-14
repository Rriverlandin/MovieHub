import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Movie


# =========================================================
# App factory / config
# =========================================================

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "moviehub_super_secret_key_2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///moviehub.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    register_error_handlers(app)

    return app


# =========================================================
# Auth helper
# =========================================================

def login_required(view):
    """Redirect to /login if there's no active session, otherwise
    inject the current user as the view's first argument."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("login"))

        user = User.query.get(user_id)
        if user is None:
            session.clear()
            flash("Your session has expired. Please log in again.", "error")
            return redirect(url_for("login"))

        return view(user, *args, **kwargs)

    return wrapped


def owned_movie_or_404(user: User, movie_id: int) -> Movie:
    """Fetch a movie by id, but only if it belongs to the current user."""
    movie = Movie.query.get_or_404(movie_id)
    if movie.user_id != user.id:
        flash("You don't have permission to do that.", "error")
        return None
    return movie


# =========================================================
# Routes
# =========================================================

def register_routes(app: Flask) -> None:

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard"))
        return render_template("index.html")

    # ---------------- Auth ----------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            confirmation = request.form.get("confirmation") or ""

            if not username or not password or not confirmation:
                flash("Please fill in all fields.", "error")
                return redirect(url_for("register"))

            if len(password) < 8:
                flash("Password must be at least 8 characters.", "error")
                return redirect(url_for("register"))

            if password != confirmation:
                flash("Passwords do not match.", "error")
                return redirect(url_for("register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists.", "error")
                return redirect(url_for("register"))

            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        session.clear()

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""

            user = User.query.filter_by(username=username).first()

            if user is None or not check_password_hash(user.password, password):
                flash("Invalid username or password.", "error")
                return redirect(url_for("login"))

            session["user_id"] = user.id
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You've been logged out.", "success")
        return redirect(url_for("index"))

    # ---------------- Dashboard ----------------

    @app.route("/dashboard")
    @login_required
    def dashboard(user: User):
        return render_template("dashboard.html", user=user)

    # ---------------- Movie CRUD ----------------

    @app.route("/movie/add", methods=["POST"])
    @login_required
    def add_movie(user: User):
        title = (request.form.get("title") or "").strip()

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("dashboard"))

        movie = Movie(user_id=user.id, title=title)
        movie.apply_form(request.form)

        db.session.add(movie)
        db.session.commit()

        flash(f'"{movie.title}" added to your collection.', "success")
        return redirect(url_for("dashboard"))

    @app.route("/movie/<int:movie_id>/edit", methods=["POST"])
    @login_required
    def edit_movie(user: User, movie_id: int):
        movie = owned_movie_or_404(user, movie_id)
        if movie is None:
            return redirect(url_for("dashboard"))

        title = (request.form.get("title") or "").strip()
        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("dashboard"))

        movie.apply_form(request.form)
        db.session.commit()

        flash(f'"{movie.title}" updated.', "success")
        return redirect(url_for("dashboard"))

    @app.route("/movie/<int:movie_id>/delete", methods=["POST"])
    @login_required
    def delete_movie(user: User, movie_id: int):
        movie = owned_movie_or_404(user, movie_id)
        if movie is None:
            return redirect(url_for("dashboard"))

        title = movie.title
        db.session.delete(movie)
        db.session.commit()

        flash(f'"{title}" deleted.', "success")
        return redirect(url_for("dashboard"))

    @app.route("/movie/<int:movie_id>/favorite", methods=["POST"])
    @login_required
    def toggle_favorite(user: User, movie_id: int):
        movie = owned_movie_or_404(user, movie_id)
        if movie is None:
            return redirect(url_for("dashboard"))

        movie.favorite = not movie.favorite
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/movie/<int:movie_id>/watched", methods=["POST"])
    @login_required
    def toggle_watched(user: User, movie_id: int):
        movie = owned_movie_or_404(user, movie_id)
        if movie is None:
            return redirect(url_for("dashboard"))

        movie.watched = not movie.watched
        db.session.commit()
        return redirect(url_for("dashboard"))


# =========================================================
# Error handlers
# =========================================================

def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("error.html", code=500, message="Something went wrong."), 500


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
