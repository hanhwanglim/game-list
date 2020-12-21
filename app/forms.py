from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """ A class that validates sign up form """
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email(message="Invalid email address.")], render_kw={
    "class":"form-control", 
    "placeholder":"Email address", 
    "autofocus":""})
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")], render_kw={"class":"form-control", "placeholder":"Username"})
    password = PasswordField('Enter password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match.')], render_kw={"class":"form-control", "placeholder":"Password", "autofocus":""})
    confirm = PasswordField('Confirm password', render_kw={"class":"form-control", 
    "placeholder":"Confirm password", 
    "autofocus":""})
    accept_tos = BooleanField('I accept the Term of Service and Privacy Policy', [validators.InputRequired()])
    submit = SubmitField("Create account", render_kw={"class":"w-100 btn btn-lg btn-primary"})


class LoginForm(FlaskForm):
    """ A class that validates login form """
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")], render_kw={
    "class":"form-control", 
    "placeholder":"Username", 
    "autofocus":""})
    password = PasswordField('Password', [validators.DataRequired()], render_kw={"class":"form-control", "placeholder":"Password", "autofocus":""})
    remember = BooleanField("Remember me?")
    submit = SubmitField("Login", render_kw={"class":"w-100 btn btn-lg btn-primary"})