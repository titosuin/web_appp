"""
Database models for the application.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    # pylint: disable=too-few-public-methods

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    onboarded = db.Column(db.Boolean, default=False)
    tour_completed = db.Column(db.Boolean, default=False)

    stats = db.relationship(
        "PhysicalStats",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    logs = db.relationship(
        "WorkoutLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )


class PhysicalStats(db.Model):
    """Physical statistics model."""

    # pylint: disable=too-few-public-methods
    __tablename__ = "physical_stats"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Measurements
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    body_fat = db.Column(db.Float, nullable=True)

    # Nutrition / Lifestyle
    activity_level = db.Column(db.String(50), default="Moderado")
    goal = db.Column(db.String(50), default="Composición")

    # RMs (Now Optional initially)
    sq_rm = db.Column(db.Float, nullable=True, default=0.0)
    bp_rm = db.Column(db.Float, nullable=True, default=0.0)
    dl_rm = db.Column(db.Float, nullable=True, default=0.0)

    # Computed Rank
    rank = db.Column(db.String(50), default="Pendiente de Test")


class Exercise(db.Model):
    """Exercise model."""

    # pylint: disable=too-few-public-methods
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(50))
    force = db.Column(db.String(50))
    equipment = db.Column(db.String(100))
    primary_muscles = db.Column(db.String(255))
    instructions = db.Column(db.Text)
    instructions_es = db.Column(db.Text)
    video_id = db.Column(db.String(50))
    category = db.Column(db.String(100))
    image_url = db.Column(db.String(255))


class WorkoutLog(db.Model):
    """Workout log model."""

    # pylint: disable=too-few-public-methods
    __tablename__ = "workout_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    status = db.Column(db.String(20), default="completed")
