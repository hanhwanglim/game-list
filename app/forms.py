from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """ A class that validates sign up form """
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email(message="Invalid email address.")])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")])
    password = PasswordField('Enter password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Confirm password')
    accept_tos = BooleanField('I have read and agree to the Term of Service and Privacy Policy', [validators.InputRequired()])


class LoginForm(FlaskForm):
    """ A class that validates login form """
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField("Always stay logged in?")