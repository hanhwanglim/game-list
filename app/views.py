from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, admin
from app.forms import *
from app.models import *
from flask_admin.contrib.sqla import ModelView
from datetime import date
from sqlalchemy import func
import json

class AdminModelView(ModelView):
    column_exclude_list = ['password']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Game, db.session))
admin.add_view(AdminModelView(Developer, db.session))
admin.add_view(AdminModelView(Publisher, db.session))
admin.add_view(AdminModelView(Genre, db.session))
admin.add_view(AdminModelView(Model, db.session))
admin.add_view(AdminModelView(Platform, db.session))


@app.route('/', methods=['GET'])
def index():
    """
    Redirects to feed if the user is already logged in.
    Otherwise it will return to the index page.
    """
    year = 2020
    # Query this year's games
    games_1 = Game.query.filter(Game.release_date < date(year + 1, 1, 1), Game.release_date >= date(year, 1, 1)).limit(10)
    # Query last year's games
    games_2 = Game.query.filter(Game.release_date < date(year, 1, 1), Game.release_date >= date(year - 1, 1, 1)).limit(10)
    # Query year before last games
    games_3 = Game.query.filter(Game.release_date < date(year - 1, 1, 1), Game.release_date >= date(year - 2, 1, 1)).limit(10)
    if current_user.get_id() is not None:
        return redirect(url_for('feed'))
    return render_template('index.html', games_1=games_1, games_2=games_2, games_3=games_3, year=year, login=current_user.is_authenticated)


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
            return render_template('signup.html', form=form, login=current_user.is_authenticated)
        elif find_user_email is not None:
            flash('Email has already exist.')
            return render_template('signup.html', form=form, login=current_user.is_authenticated)
        elif find_user_username is not None:
            flash('Username has already been taken.')
            return render_template('signup.html', form=form, login=current_user.is_authenticated)

        # Adding user into the user database
        user = User(email=new_email, username=new_username, password=generate_password_hash(new_password, method='sha256'))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template('signup.html', form=form, login=current_user.is_authenticated)


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
            return render_template("login.html", form=form, login=current_user.is_authenticated)
        # Create a session and redirect to feed
        login_user(user, remember=remember)
        return redirect(url_for('feed'))
    return render_template('login.html', form=form, login=current_user.is_authenticated)


@app.route('/feed')
@login_required
def feed():
    """
    The user's feed page. It shows the user's game lists and shows other random games in the
    game database for the user to checkout
    """
    games = current_user.games
    random = Game.query.filter_by().order_by(func.random()).limit(5)
    return render_template('feed.html', user=current_user, games=games, checkout=random, login=current_user.is_authenticated)


@app.route('/add', methods=['POST'])
@login_required
def add():
    """
    A route to handle the response from AJAX to add a game to the user's game list.
    """
    # Handling response from AJAX
    data = json.loads(request.data)
    response = data.get('response')
    index = response.find('_')
    game_id = int(response[index + 1 : ])
    # Find the game in the database
    game = Game.query.get(game_id)
    # Update user's game list
    if not game in current_user.games:
        current_user.games.append(game)
        db.session.add(current_user)
        db.session.commit()
    return json.dumps({'status': 'OK', 'response': game_id})


@app.route('/remove', methods=['POST'])
@login_required
def remove():
    """
    A route to handle the response from AJAX to remove a game from the user's game list.
    """
    # Handling response from AJAX
    data = json.loads(request.data)
    response = data.get('response')
    index = response.find('_')
    game_id = int(response[index + 1 : ])
    # Find game in the database
    game = Game.query.get(game_id)
    # Update user's game list
    if game in current_user.games:
        current_user.games.remove(game)
        db.session.add(current_user)
        db.session.commit()
    return json.dumps({'status': 'OK', 'response': game_id})


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    A route to display the search query from a user. Returns similar games from the query
    """
    if request.form.get("search") is not None:
        query = request.form.get("search")
        search_query = "%" + query + "%"
        games = Game.query.filter(Game.title.like(search_query)).limit(10).all()
        return render_template('search.html', query=query, games=games, login=current_user.is_authenticated)
    return redirect(url_for("index"))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def setting():
    form = PasswordForm()
    if form.validate_on_submit():
        old_password = request.form.get("old_password")
        if check_password_hash(current_user.password, old_password):
            new_password = request.form.get("password")
            current_user.password = generate_password_hash(new_password)
            db.session.add(current_user)
            db.session.commit()
            flash("Password updated successfully.")
            return render_template('setting.html', form=form, login=current_user.is_authenticated)
        else:
            flash("Password incorrect.")
            return render_template('setting.html', form=form, login=current_user.is_authenticated)
    return render_template('setting.html', form=form, login=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    """ Logs the user out of the session """
    logout_user()
    return redirect(url_for('index'))