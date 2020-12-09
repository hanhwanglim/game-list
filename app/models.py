from app import db


class User(db.Model):
    """ A class that stores user details in the database """
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.username
