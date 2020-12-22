import os


WTF_CSRF_ENABLED = True
SECRET_KEY = 'IfRJbXqxMq6GTK1B'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True    
