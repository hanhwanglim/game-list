from app import db
from flask_login import UserMixin

# Many-to-Many relationships
user_game = db.Table('user_game', db.Model.metadata,
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('user.user_id')),
                     db.Column('game_id', db.Integer,
                               db.ForeignKey('game.game_id'))
                     )

game_genre = db.Table('game_genre', db.Model.metadata,
                      db.Column('game_id', db.Integer,
                                db.ForeignKey('game.game_id')),
                      db.Column('genre_id', db.Integer,
                                db.ForeignKey('genre.genre_id'))
                      )

game_model = db.Table('game_model', db.Model.metadata,
                      db.Column('game_id', db.Integer,
                                db.ForeignKey('game.game_id')),
                      db.Column('model_id', db.Integer,
                                db.ForeignKey('model.model_id'))
                      )

game_platform = db.Table('game_platform', db.Model.metadata,
                         db.Column('game_id', db.Integer,
                                   db.ForeignKey('game.game_id')),
                         db.Column('platform_id', db.Integer,
                                   db.ForeignKey(
                                       'platform.platform_id'))
                         )


class User(UserMixin, db.Model):
    """
    A class that stores user details in the database

    Attributes
        user_id:    Stores the User ID
        email:      Stores the user's email address
        username:   Stores the user's username
        password:   Stores the user's encrypted password
        admin:      Stores the user's account type
        games:      Stores the user's list of games
    """
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    games = db.relationship('Game', secondary=user_game)

    def __repr__(self):
        """
        :return: username
        """
        return self.username

    def get_id(self):
        """
        :return: user_id
        """
        return self.user_id

    def is_admin(self):
        """
        :return: admin
        """
        return self.admin


class Game(db.Model):
    """ 
    A class that stores game details in the database 
    
    Attributes
        game_id:        Stores the Game ID
        title:          Stores the game's title
        description:    Stores the game's description
        release_date:   Stores the game's release date
        developer:      Stores the game's developer ID
        publisher:      Stores the game's publisher ID
        genre:          Stores the game's list of genres
        model:          Stores the game's list of models
        platform:       Stores the game's list of platforms
    """
    game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    release_date = db.Column(db.Date, nullable=False)
    developer = db.Column(db.Integer,
                          db.ForeignKey('developer.developer_id'))
    publisher = db.Column(db.Integer,
                          db.ForeignKey('publisher.publisher_id'))
    genre = db.relationship('Genre', secondary=game_genre,
                            backref='game_genre')
    model = db.relationship('Model', secondary=game_model,
                            backref='game_model')
    platform = db.relationship('Platform', secondary=game_platform,
                               backref='game_platform')

    def __repr__(self):
        """
        :return: title
        """
        return self.title

    def genre_to_string(self):
        """
        :return: genre list to string
        """
        return str(self.genre)[1:-1]

    def model_to_string(self):
        """
        :return: model list to string
        """
        return str(self.model)[1:-1]

    def platform_to_string(self):
        """
        :return: platform list to string
        """
        return str(self.platform)[1:-1]


class Developer(db.Model):
    """ 
    A class that stores developer details in the database 
    
    Attributes
        developer_id:   Stores the Developer's ID
        name:           Stores the developer's name
        games:          Stores the developer's list of games
    """
    developer_id = db.Column(db.Integer, primary_key=True,
                             nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    games = db.relationship('Game', backref='developer_name')

    def __repr__(self):
        """
        :return: name
        """
        return self.name


class Publisher(db.Model):
    """ 
    A class that stores publisher details in the database 
    
    Attributes
        publisher_id:   Stores the Publisher's ID
        name:           Stores the publisher's name
        games:          Stores the publisher's list of games
    """
    publisher_id = db.Column(db.Integer, primary_key=True,
                             nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    games = db.relationship('Game', backref='publisher_name')

    def __repr__(self):
        """
        :return: name
        """
        return self.name


class Genre(db.Model):
    """ 
    A class that stores genre details in the database
    
    Attributes
        genre_id:   Stores the Genre ID
        genre_type: Stores the genre type
    """
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre_type = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        """
        :return: genre_type
        """
        return self.genre_type


class Model(db.Model):
    """ 
    A class that stores model details in the database

    Attributes
        model_id:   Stores the Model ID
        model_type: Stores the model type
    """
    model_id = db.Column(db.Integer, primary_key=True, nullable=False)
    model_type = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        """
        :return: model_type
        """
        return self.model_type


class Platform(db.Model):
    """ 
    A class that stores platform details in the database

    Attributes
        platform_id:    Stores the Platform ID
        platform_name:  Stores the platform type
    """
    platform_id = db.Column(db.Integer, primary_key=True,
                            nullable=False)
    platform_name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        """
        :return: platform_name
        """
        return self.platform_name
