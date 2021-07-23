from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)
# @views.route('/')
# @login_required
# def home():
#    return render_template("home.html", user=current_user)

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

# route and function to handle the upload page
@views.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
      if request.form.get('note') is not None:
         note = request.form.get('note')
         input_note = note
         if len(note) < 1:
            flash('Note is too short!', category='error')
         else:
            neighbor_count = {}
            note = "".join(char for char in note if char not in ('!','.',':','.',",","^","/","!","$","%","*",";",":",")","(","[")).lower()
            words = note.split()
            print(words)
            for index, word in enumerate(words):
               if index+1 < len(words):
                        if word > words[index+1]:
                           wordPair = (word, words[index+1])
                        else:
                           wordPair = (words[index+1], word)
                        if wordPair in neighbor_count:
                           neighbor_count[wordPair] += 1
                        else:
                           neighbor_count[wordPair]  = 1
            neighbor_count = str(neighbor_count)
            new_note = Note(data=neighbor_count, input=input_note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
      # check if there is a file in the request
      if 'file' not in request.files:
         return render_template('home.html', msg='No file selected',user=current_user)
      file = request.files['file']
      # if no file is selected
      if file.filename == '':
         return render_template('home.html', msg='No file selected', user=current_user)
      print(file.filename)
      if file and allowed_file(file.filename):

         # call the OCR function on it
         extracted_text = ocr_core(file)
         print(extracted_text)
         # extract the text and display it
         return render_template('home.html', user=current_user,
                                 msg='Successfully processed',
                                 extracted_text=extracted_text,
                                 img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('home.html',user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/reuse-note', methods=['POST'])
def reuse_note():
    flash('Input copied!', category='success')
    return jsonify({})
