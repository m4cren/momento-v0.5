from flask import Flask
from .extensions import db, DB_NAME
from .sockets import socketio
from os import path
from flask_login import LoginManager







def create_website():
     app = Flask(__name__)
     app.config['SECRET_KEY'] = 'aki7-29-05_kyle3-01-05_mika6-10-05_anne9-8-04_ren10-27-04'
     app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
     

     db.init_app(app)
     socketio.init_app(app)


     from .views import views
     from .auth import auth

     from .models import Posts, User, Comments, UserLikedPosts

     create_database(app)

     app.register_blueprint(views, url_prefix = '/')
     app.register_blueprint(auth, url_prefix = '/')

     login_manager = LoginManager()
     login_manager.login_view = 'views.index_page'
     login_manager.init_app(app)

     @login_manager.user_loader
     def load_user(id):
          return User.query.get(int(id))
     
     
     return app

def create_database(app):
     if not path.exists('app' + DB_NAME):
          with app.app_context():
               db.create_all()
               print("Created Database!")