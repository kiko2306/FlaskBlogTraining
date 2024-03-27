from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()

def create_app():
    # create the app
    app=Flask(__name__)
    app.config['SECRET_KEY']= "carol"
    # configure the SQLite database, relative to the app instance folder
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///database.db'
    # initialize the app with the extension
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # getting information about the logged user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app  

def create_database(app):
    with app.app_context():
        # if not path.exists("website/database.db"):
        db.create_all()
        print("Created database!")