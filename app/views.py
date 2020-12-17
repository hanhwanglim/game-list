from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, admin
from app.forms import *
from app.models import *
from flask_admin.contrib.sqla import ModelView
from datetime import date
from sqlalchemy import func


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(Developer, db.session))
admin.add_view(ModelView(Publisher, db.session))
admin.add_view(ModelView(Genre, db.session))
admin.add_view(ModelView(Model, db.session))
admin.add_view(ModelView(Platform, db.session))


@app.route('/', methods=['GET'])
def index():
    """
    Redirects to feed if the user is already logged in.
    Otherwise it will return to the index page.
    """
    year = date.today().year
    games_1 = Game.query.filter(Game.release_date < date(year + 1, 1, 1), Game.release_date >= date(year, 1, 1)).limit(10)
    games_2 = Game.query.filter(Game.release_date < date(year, 1, 1), Game.release_date >= date(year - 1, 1, 1)).limit(10)
    games_3 = Game.query.filter(Game.release_date < date(year - 1, 1, 1), Game.release_date >= date(year - 2, 1, 1)).limit(10)
    if current_user.get_id() is not None:
        return redirect(url_for('feed'))
    return render_template('index.html', games_1=games_1, games_2=games_2, games_3=games_3, year=year)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Redirects to signup.html if the request method is a GET method.
    Otherwise, if the request method is a POST method, then it will 
    create a new user with the user details and add it into the database.
    Then, redirects them to login.
    """
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

        return redirect(url_for("login"))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Redirects to login.html if the request method is a GET method.
    Otherwise, if the request method is a POST method, then it will 
    query and verify the user and return to their feed.
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash("Username or password incorrect.")
            return render_template("login.html", form=form)
        # Create a session and redirect to feed
        login_user(user, remember=remember)
        return redirect(url_for('feed'))
    return render_template('login.html', form=form)


@app.route('/feed')
@login_required
def feed():
    games = current_user.games
    random = Game.query.filter_by().order_by(func.random()).limit(5)
    return render_template('feed.html', user=current_user, games=games, checkout=random)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.form is not None:
        query = request.form.get('search')
        search_query = "%" + request.form.get('search') + "%"
        print(query)
        games = Game.query.filter(Game.title.like(search_query)).limit(10).all()
        developers = Developer.query.filter(Developer.name.like(search_query)).limit(10).all()
        publishers = Publisher.query.filter(Publisher.name.like(search_query)).limit(10).all()
        genres = Genre.query.filter(Genre.genre_type.like(search_query)).limit(10).all()
        print(games)
        return render_template('search.html', query=query, games=games, developers=developers, publishers=publishers, genres=genres)
    return render_template('search.html')



@app.route('/logout')
@login_required
def logout():
    """ Logs the user out of the session """
    logout_user()
    return redirect(url_for('index'))