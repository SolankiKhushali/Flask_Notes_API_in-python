from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
import os
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Print data from server
        data = request.form
        print(data)
        it will print this :ImmutableMultiDict([('email', 'tim@gmail'), ('password', '123455656566')]) 
            if we have enterd email and password in input fields of login form!
        ORELSE it will return ImmutableMultiDict([]) like this when the page gets refreshes!
        ORELSE it can also return: ImmutableMultiDict([('email', ''), ('password', '')]) like this when we have pressed the button 
            without filling the from!
                return render_template("login.html", boolean = "abc")   """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_user_by_email(current_app.db, email)

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Login success!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password!', category='error')
            
    return render_template('login.html', user = current_user)
        # return print("data added succesfully")
        # email = request.form.get('email')
        # password = request.form.get('password')
        # user = User.db(db).get_user_by_email(email)
        # if user and user['password'] == password:
        #     login_user(user)
        #     return redirect(url_for('views.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
            return render_template("signup.html")
        elif firstName is None or len(firstName) < 2:
            flash('firstName must be greater than 2 characters.', category='error')
            return render_template("signup.html")
        elif len(password1) < 7:
            flash('password must be greater than 7 characters.', category='error')
            return render_template("signup.html")
        elif len(password2) < 7:
            flash('Confirm your password!', category='error')
            return render_template("signup.html")
        elif password1 != password2:
            flash("Password doesn't match!", category='error')
            return render_template("signup.html")
        else:
            existing_user = User.get_user_by_email(current_app.db, email)
            if existing_user:
                flash('Email Address already exists!', category='error')
                return render_template("login.html")
            hashed_password = generate_password_hash(password1, method='sha256')
            user = User.add_user(current_app.db, email, hashed_password, firstName)
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)