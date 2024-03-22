from flask import Blueprint, render_template, redirect, url_for

auth= Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home")) #when I redirect to a function I can change the url and I won't loose the connection