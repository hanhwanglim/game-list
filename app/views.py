from flask import render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import RegisterForm, LoginForm
from app.models import User


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        # Find if username or email is in database
        new_email = request.form.get("email")
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        find_user_email = User.query.filter(User.email==new_email).first()
        find_user_username = User.query.filter(User.username==new_username).first()

        # If a user with the same email or username is found then return error
        if find_user_email and find_user_username is not None:
            flash('Username and email has already exist.')
            return render_template('signup.html', form=form)
        elif find_user_email is not None:
            flash('Email has already exist.')
            return render_template('signup.html', form=form)
        elif find_user_username is not None:
            flash('Username has already been taken.')
            return render_template('signup.html', form=form)
            
        # Adding user into the user database
        user = User(email=new_email, username=new_username, password=generate_password_hash(new_password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return "success"
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("hello")
        return "hello"
    return render_template('login.html', form=form)