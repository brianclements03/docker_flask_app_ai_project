#all route logic goes in this file

from flask import Blueprint, current_app, render_template
from app.models import db, MyTable #adjust model name as needed
import os
from flask import request, redirect, url_for, flash


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


#new functionality 8jun2025 to add a file-upload functionality to the app

UPLOAD_FOLDER = '/flask-app/uploads'  # this is inside the container

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # return "No file part", 400 #updating this to flash instead of landing on white page
        flash("No file part")
        return redirect(url_for('main.home'))

    file = request.files['file']
    if file.filename == '':
        # return "No selected file", 400 #ditto above
        flash("No selected file")
        return redirect(url_for('main.home'))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # return f"File '{file.filename}' uploaded successfully!"
    flash(f"File '{file.filename}' uploaded successfully!")
    return redirect(url_for('main.home'))





