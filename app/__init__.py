# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.db_model import db
from decouple import config
import sqlalchemy.exc
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # centralized config
    db.init_app(app)

    # Register routes via Blueprints
    from app.routes import main, query  # <-- import both
    app.register_blueprint(main.main)   # <-- use the Blueprint name, not module
    app.register_blueprint(query.query)

    # Wait for DB and create tables
    with app.app_context():
        max_retries = 10
        for attempt in range(max_retries):
            try:
                db.create_all()
                print("✅ Database is ready.")
                break
            except sqlalchemy.exc.OperationalError as e:
                print(f"⏳ DB not ready ({attempt+1}/{max_retries}): {e}. Retrying in 2 sec...")
                time.sleep(2)
        else:
            raise RuntimeError("❌ Failed to connect to the DB after multiple retries.")

    return app
