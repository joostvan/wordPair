from flask import render_template, Blueprint, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth = Blueprint('auth',__name__)
# decerator for signup
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.render_text_page'))

    return render_template("signup.html", user=current_user)
    
# decerator for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.render_text_page'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# decerator for logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import pytesseract
from PIL import Image
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# # route and function to handle the upload page
# @auth.route('/', methods=['GET', 'POST'])
# def upload_page():
#     if request.method == 'POST':
#         # check if there is a file in the request
#         if 'file' not in request.files:
#             return render_template('home.html', msg='No file selected')
#         file = request.files['file']
#         # if no file is selected
#         if file.filename == '':
#             return render_template('home.html', msg='No file selected')
#         print(file.filename)
#         if file and allowed_file(file.filename):

#             # call the OCR function on it
#             extracted_text = ocr_core(file)
#             print(extracted_text)
#             # extract the text and display it
#             return render_template('upload.html',
#                                    msg='Successfully processed',
#                                    extracted_text=extracted_text,
#                                    img_src=UPLOAD_FOLDER + file.filename)
#     elif request.method == 'GET':
#         return render_template('home.html')