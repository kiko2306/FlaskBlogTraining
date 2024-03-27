from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

auth= Blueprint("auth", __name__)

@auth.route("/login", methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email= request.form.get("email")
        password= request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                flash("Logged in!", category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash("Password is incorrect.", category='error')
        else:
            flash("Email does not exist.", category='error')

    return render_template("login.html", user=current_user)

@auth.route("/sign_up", methods= ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email= request.form.get("email")
        username= request.form.get("username")
        password1= request.form.get("password1")
        password2= request.form.get("password2")

        email_exists= User.query.filter_by (email=email).first()
        username_exists= User.query.filter_by (username=username).first()
        if email_exists:
            flash("Email i already in use.", category='error')
        elif username_exists:
            flash("Username is alredy in use", category='error')
        elif password1 != password2:
            flash("Password don't match!", category='error')
        elif len(username) < 2:
            flash("Username is too short.", category='error')
        elif len(password1) < 6:
            flash("Password is too short.", category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            new_user = User(email=email, username=username, password=hashed_password.decode('utf-8'))
            db.session.add(new_user)
            db.session.commit()
            flash("User created!")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home')) # when I redirect to a function I can change the url and I won't loose the connection