from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import pytesseract
from PIL import Image
import json

views = Blueprint('views', __name__)
# set designated upload folder and, allowed extensions
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# allow files of a specific extension
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# function to check the file extension
def allowed_file(filename):
   '''
   check to see if filename is in allowed extensions
   input: filename, String
   returns: Boolean
   '''
   return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_core(filename):
    '''
    OCR Processing of images using Pytesseract
    input: filename, String
    returns: String
    '''
    text = pytesseract.image_to_string(Image.open(filename))  
    return text

# route and function to handle the main page
@views.route('/', methods=['GET', 'POST'])
@login_required
def render_text_page():
   '''
   called on when on main page, renders post and get requests.
   Also calculates wordPairs by enumerating array words and comparing to dictionary

   '''
   if request.method == 'POST':
      if request.form.get('note') is not None:
         note = request.form.get('note')
         input_note = note
         if len(note) < 1:
            flash('Note is too short!', category='error')
         else:
            # set neighbor_count as dictionary
            neighbor_count = {}
            note = "".join(char for char in note if char not in ('!','.',':','.',",","^","/","!","$","%","*",";",":",")","(","[")).lower()
            #split string into array of words
            words = note.split()
            # iterate through words
            for index, word in enumerate(words):
               # set out bounds on array iteration
               if index+1 < len(words):
                        # find pairs of different words
                        if word > words[index+1]:
                           wordPair = (word, words[index+1])
                        else:
                           wordPair = (words[index+1], word)
                        # update dictionary if wordPair already exists
                        if wordPair in neighbor_count:
                           neighbor_count[wordPair] += 1
                        else:
                           neighbor_count[wordPair]  = 1
            # caste to string
            neighbor_count = str(neighbor_count)
            # make note of it
            new_note = Note(data=neighbor_count, input=input_note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Input added!', category='success')
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
   '''
   Deletes the requested note input by json loading a request of the data. 
   If we are indeed the current user, then we can delete the note.
   Returns: an empty json response

   '''
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
   '''
   Flashes a response when the input note is copied
   Returns: an empty json response

   '''
   flash('Input copied!', category='success')
   return jsonify({})
