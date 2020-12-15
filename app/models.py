from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """ A class that stores user details in the database """
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.username

    
    def get_id(self):
        return self.user_id

    
    def is_admin(self):
        return self.admin
