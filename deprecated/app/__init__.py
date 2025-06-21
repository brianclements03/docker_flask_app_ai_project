# even newer app using blueprint from app.routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db #import the db instance
from decouple import config
import sqlalchemy.exc
import time

def create_app():
    app = Flask(__name__)

    # Load DB configuration from environment
    app.config['DB_USER'] = config('DB_USER', default='root')
    app.config['DB_PASSWORD'] = config('DB_PASSWORD', default='password')
    app.config['DB_HOST'] = config('DB_HOST', default='localhost')
    app.config['DB_PORT'] = config('DB_PORT', default='3306')
    app.config['DB_NAME'] = config('DB_NAME', default='flaskapp')

    # Configure SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints here
    from app.routes import main #import the Blueprint
    app.register_blueprint(main) #register the Blueprint
    
    #auto-create schema
    with app.app_context():
        max_retries = 10
        for attempt in range(max_retries):
            try:
                db.create_all()
                print("Database is ready.")
                break
            except sqlalchemy.exc.OperationalError as e:
                print(f"Database not yet ready ({attempt+1}/{max_retries}): {e}. Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Failed to connect to the database after multiple retries.")
                raise

    app.secret_key = config('SECRET_KEY', default='supersecretkey')

    return app
