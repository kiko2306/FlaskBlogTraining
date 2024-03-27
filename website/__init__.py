from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db=SQLAlchemy()
DB_NAME = "database.db"


#create a flask application
def create_app():
    # create the app
    app=Flask(__name__)
    app.config['SECRET_KEY']= "carol"
    # configure the SQLite database, relative to the app instance folder
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    # initialize the app with the extension
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    # this is the function that creates the database with sqlalchemy 3
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    # getting information about the logged user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# this is the old way to create the database with alchemy 2
#def create_database(app):
#    if not path.exists("website/" + DB_NAME):
#        db.create_all(app = app)
#        print("Created database!")
