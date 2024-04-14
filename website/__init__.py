from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # Setting up the website with app name and key
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    from .models import Doctor, Patient, Diagnosis

    create_database(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')    #for prefix you can set url like/auth/hello

    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_up_page' # Where to go if not logged in
    login_manager.init_app(app)               # Telling login manager which app to work in

    @login_manager.user_loader
    def load_user(id):
        return Doctor.query.get(int(id)) or Patient.query.get(int(id))
     
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
