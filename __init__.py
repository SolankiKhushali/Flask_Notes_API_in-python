from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager, current_user

from website.models import User, Note

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyopenkey openkeyqwerty'
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Add_Note_db"
    # db = PyMongo(app).db
    mongo = PyMongo(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    
    @login_manager.user_loader # type: ignore
    def load_user(id):
        return User.get_user_by_id(app.db, id)

    app.db = mongo.db

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app

