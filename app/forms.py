from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """ A class that validates sign up form """
    email = EmailField('email', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email()])
    username = StringField('username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('repeat')
    accept_tos = BooleanField('tos', [validators.InputRequired()])


class LoginForm(FlaskForm):
    """ A class that validates login form """
    username = StringField('username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired()])