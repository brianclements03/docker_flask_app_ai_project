#all route logic goes in this file

from flask import Blueprint, current_app, render_template
from app.models import db, MyTable #adjust model name as needed
import os
from flask import request, redirect, url_for, flash, current_app
import pandas as pd
from app.models import db, MyTable
import openpyxl

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#main app functionality: display web app
main = Blueprint('main', __name__)

@main.route('/')
def home():
    try:
        port = current_app.config.get('PORT', 5000)
        users = MyTable.query.all() #fetch all records. MAKE SURE THE MODEL NAME MATCHES
        return render_template('home.html', port=port,users=users)
    except Exception as e:
        return f"Error loading homepage: {e}", 500


#new functionality to add file-upload functionality
UPLOAD_FOLDER = '/flask-app/uploads'  # this is inside the container

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # use flash functionality instead of landing on white page
        flash("No file part", "upload")
        return redirect(url_for('main.home'))

    file = request.files['file']

    if file.filename == '':
        #ditto above
        flash("No selected file", "upload")
        return redirect(url_for('main.home'))
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    #parse the newly uploaded data file
    try:
        df = pd.read_excel(filepath, engine="openpyxl")

        for _, row in df.iterrows():
            user = MyTable(name=row['name'], email=row['email'])
            db.session.add(user)

        db.session.commit()
        flash(f"File '{file.filename}' uploaded and {len(df)} records inserted!", "upload")
    except Exception as e:
        flash(f"Failed to process file: {e}", "upload")
    
    return redirect(url_for('main.home'))

# manually add a user using a form in the html
@main.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        flash('Name and email are required.', 'add_user')
        return redirect(url_for('main.home'))

    try:
        new_user = MyTable(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{name}' added successfully!", 'add_user')
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to add user: {e}", 'add_user')

    return redirect(url_for('main.home'))
