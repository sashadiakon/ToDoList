from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_migrate import Migrate

from .models import User, db
from .auth import auth as auth_blueprint
from .main import main as main_blueprint

# init SQLAlchemy so we can use it later in our models
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.name = 'Guest'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.anonymous_user = Anonymous

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    return app


with create_app().app_context():
    db.create_all()