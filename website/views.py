from flask import Blueprint, render_template
from flask_login import login_required, current_user

views= Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html", user=current_user)