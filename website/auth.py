import email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user =User.query.filter_by(email=email).first() #find user with specific email
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                return redirect( url_for('views.home'))
            else:
                flash('Incorrect password or email, try again.', category='error')
        else:
            flash('Email doesn\'t exist yet!',category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user =User.query.filter_by(email=email).first() #find user with specific email
        if user:
            flash('Email alredy exist.',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 character',category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character',category='error')
        elif password1 != password2:
            flash('Password doesn\'t match.',category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.',category='error')
        else:
            # add user to database
            new_user = User(email=email,first_name=first_name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Account created.',category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)