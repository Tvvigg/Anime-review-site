from enum import unique
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    
    favoritesList = db.relationship("Favorites", backref="User")
    reviews = db.relationship("Reviews", backref="User")

    # start of convenience class methods

    @classmethod
    def register(cls, username, password):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Favorites(db.Model):
    """User Favorites"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    anime_id = db.Column(db.String, db.ForeignKey("anime.name"), nullable=False)

class Reviews(db.Model):
    """Reviews"""

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    anime_id = db.Column(db.String, db.ForeignKey("anime.name"), nullable=False)
    comments = db.Column(db.String, nullable=True)
    rating = db.Column(db.Integer, nullable=False)

class Anime(db.Model):
    """Anime List"""
    __tablename__ = "anime"
    name = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    anime_DB_id = db.Column(db.Integer, nullable=False, unique=True)
    reviews = db.relationship("Reviews", backref="anime")



