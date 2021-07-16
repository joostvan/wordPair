from flask import Blueprint, render_template, request, jsonify
views = Blueprint('views', __name__)
@views.route('/')
def home():
    return render_template("home.html")

@views.route('/sign-up')
def signup():
    return render_template("signup.html")
    
@views.route('/login')
def login():
    return render_template("login.html")

@views.route('/logout')
def logout():
    return render_template("logout.html")