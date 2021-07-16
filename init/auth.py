from flask import render_template, Blueprint, flash, request
auth = Blueprint('auth',__name__)

# decerator for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

# decerator for logout
@auth.route('/logout')
def logout():
    return render_template("logout.html")

# decerator for signup
@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')
    return render_template("signup.html")
