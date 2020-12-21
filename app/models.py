from app import db
from flask_login import UserMixin

# Relationship
user_game = db.Table('user_game', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.game_id'))
)

game_genre = db.Table('game_genre', db.Model.metadata,
    db.Column('game_id', db.Integer, db.ForeignKey('game.game_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'))
)

game_model = db.Table('game_model', db.Model.metadata,
    db.Column('game_id', db.Integer, db.ForeignKey('game.game_id')),
    db.Column('model_id', db.Integer, db.ForeignKey('model.model_id'))
)

game_platform = db.Table('game_platform', db.Model.metadata,
    db.Column('game_id', db.Integer, db.ForeignKey('game.game_id')),
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.platform_id'))
)

class User(UserMixin, db.Model):
    """ A class that stores user details in the database """
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    games = db.relationship('Game', secondary=user_game)

    def __repr__(self):
        return self.username

    
    def get_id(self):
        return self.user_id

    
    def is_admin(self):
        return self.admin


class Game(db.Model):
    """ A class that stores game details in the database """
    game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    release_date = db.Column(db.Date, nullable=False)
    developer = db.Column(db.Integer, db.ForeignKey('developer.developer_id'))
    publisher = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'))
    genre = db.relationship('Genre', secondary=game_genre, backref='game_genre')
    model = db.relationship('Model', secondary=game_model, backref='game_model')
    platform = db.relationship('Platform', secondary=game_platform, backref='game_platform')

    def __repr__(self):
        return self.title


class Developer(db.Model):
    """ A class that stores developer details in the database """
    developer_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    games = db.relationship('Game', backref='developer_name')

    def __repr__(self):
        return self.name


class Publisher(db.Model):
    """ A class that stores publisher details in the database """
    publisher_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    games = db.relationship('Game', backref='publisher_name')

    def __repr__(self):
        return self.name


class Genre(db.Model):
    """ A class that stores genre details in the database """
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre_type = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return self.genre_type


class Model(db.Model):
    """ A class that stores model details in the database """
    model_id = db.Column(db.Integer, primary_key=True, nullable=False)
    model_type = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return self.model_type


class Platform(db.Model):
    """ A class that stores platform details in the database """
    platform_id = db.Column(db.Integer, primary_key=True, nullable=False)
    platform_name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return self.platform_name
    