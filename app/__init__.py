from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager

app=Flask(__name__)
app.config.from_object('config')

# Database 
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app,template_mode='bootstrap3')


from app import views, models
from app.models import User

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = None
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))