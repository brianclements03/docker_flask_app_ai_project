#all route logic goes in this file

from flask import Blueprint, current_app, render_template
from app.models import db, MyTable #adjust model name as needed

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # from app.models import MyTable #adjust model name as needed
    # from app import db
    try:
        port = current_app.config.get('PORT', 5000)
        users = MyTable.query.all() #fetch all records. MAKE SURE THE MODEL NAME MATCHES
        return render_template('home.html', port=port,users=users)
    except Exception as e:
        return f"Error loading homepage: {e}", 500





# a good udf to render the simple webpage, from an earlier version

# def setup_routes(app):
#     @app.route('/')
#     def home():
#         try:
#             port = app.config.get('PORT', 5000)
#             return f"Running on port {port}"
#         except Exception as e:
#             return f"PORT variable missing: {e}", 500

