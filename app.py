"""
Main application module.
"""

import os
from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from models import db
from routes import register_routes

app = Flask(__name__)

# Security & Setup
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
db_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "instance", "ironmind.db"
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Server Side Session config
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

with app.app_context():
    # Make sure instance dir exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db.create_all()
    
    # Auto-seed the database if empty on Docker/Windows start
    from seed_exercises import seed
    seed()

register_routes(app, db, socketio)

if __name__ == "__main__":
    socketio.run(
        app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True
    )
