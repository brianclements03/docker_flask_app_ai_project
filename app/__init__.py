# even newer app using blueprint from app.routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db #import the db instance
from decouple import config
# import os
import sqlalchemy.exc
import time

# db = SQLAlchemy() #globally accessible db obj

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
    
#     (
#         f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#         f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
#     )
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
    #  db.create_all()

    app.secret_key = config('SECRET_KEY', default='supersecretkey')

    return app





# #new flask app.py
# from flask import Flask
# # from decouple import config
# from decouple import AutoConfig
# # get routes from .routes file
# from .routes import setup_routes

# #create the app using UDF
# def create_app():
#      app = Flask(__name__)
# # PORT = config('PORT',default=5000)
# # config = AutoConfig(failure_cast=True) #this line seems to be problematic--the failure_cast=True part
#      config = AutoConfig(search_path='.')
     
#      app.config['PORT'] = config('PORT', default = 5000)
#      setup_routes(app)

#      return app


# the below pertains to an earlier version of the app
# @app.route('/')
# def home():
#      # return "Hello, Docker!"
#      try:
#           port = config('PORT')
#           return f"Running on port {port}"
#      except Exception as e:
#           return f"PORT variable missing: {e}", 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
