import json
import os.path as op
from datetime import date

from app import app, db
from app.forms import RegisterForm, LoginForm, PasswordForm
from app.models import Game, User, Developer, Publisher, Genre, Model, \
    Platform
from flask import render_template, request, flash, url_for, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user, \
    current_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash, \
    check_password_hash


class AdminView(AdminIndexView):
    """
    A class that limits the admin page for admin users only. Users 
    without permission will be displayed an Error:403 page
    """

    def is_accessible(self):
        """
        Allow admin route to be accessed by verified administrators.

        :return: True if user is a verified admin.
        """
        return current_user.is_authenticated and current_user.is_admin()


class AdminModelView(ModelView):
    """
    A class that limits the admin page for admin users only. The admin
    are not able to see the password column for users.
    """
    column_exclude_list = ['password']


class UploadImages(FileAdmin):
    """
    A class that limits the admin page for admin users only. The admin
    is able to upload image files.
    """
    allowed_extensions = {'png', 'jpg', 'jpeg'}


admin = Admin(app, template_mode='bootstrap4', index_view=AdminView())
# Setting what database can the admin view
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Game, db.session))
admin.add_view(AdminModelView(Developer, db.session))
admin.add_view(AdminModelView(Publisher, db.session))
admin.add_view(AdminModelView(Genre, db.session))
admin.add_view(AdminModelView(Model, db.session))
admin.add_view(AdminModelView(Platform, db.session))
path = op.join(op.dirname(__file__), 'static/game image')
admin.add_view(UploadImages(path, '/game image/', name='Game images'))


@app.route('/', methods=['GET'])
def index():
    """
    The index page contains a list of the game made in the current year,
    last year and year before last. Three types of games are queried,
    this year's games, last year's games and the year before last games.
    The games are queried and displayed in the index page

    :return: Redirects to personalised feed if user is logged in,
             otherwise to the index page of the application
    """
    # Setting up time frames
    year = date.today().year
    start_of_next_year = date(year + 1, 1, 1)
    start_of_year = date(year, 1, 1)
    start_of_last_year = date(year - 1, 1, 1)
    start_of_last_last_year = date(year - 2, 1, 1)

    # Query this year's games
    games_1 = Game.query.filter(
        Game.release_date < start_of_next_year,
        Game.release_date >= start_of_year).order_by(
        func.random()).limit(10)
    # Query last year's games
    games_2 = Game.query.filter(Game.release_date < start_of_year,
                                Game.release_date >= start_of_last_year).order_by(
        func.random()).limit(10)
    # Query year before last games
    games_3 = Game.query.filter(
        Game.release_date < start_of_last_year,
        Game.release_date >= start_of_last_last_year).order_by(
        func.random()).limit(10)
    if current_user.get_id() is not None:
        return redirect(url_for('feed'))
    return render_template('index.html', games_1=games_1,
                           games_2=games_2, games_3=games_3, year=year,
                           login=current_user.is_authenticated)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    The sign up page contains a form for the user to register
    themselves. The form is then validated using the register form in
    forms.py. The details of the registering user is then checked with
    the database to see if any existing user with the same email and
    username is used. If no users are found, then password is encrypted
    and a new user is created and stored in the database. Any errors
    would be flashed to the user.

    :return: Redirects to login page if user has successfully
             registered, otherwise flash errors messages to user.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        new_email = request.form.get('email')
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        # Find if username or email is in database
        find_user_email = User.query.filter(
            User.email == new_email).first()
        find_user_username = User.query.filter(
            User.username == new_username).first()

        # Flash error if user with email and username is found
        if find_user_email and find_user_username is not None:
            flash("Username and email has already exist.")
            return render_template('signup.html', form=form,
                                   login=current_user.is_authenticated)
        elif find_user_email is not None:
            flash("Email has already exist.")
            return render_template('signup.html', form=form,
                                   login=current_user.is_authenticated)
        elif find_user_username is not None:
            flash("Username has already been taken.")
            return render_template('signup.html', form=form,
                                   login=current_user.is_authenticated)

        # Adding user into the user database
        user = User(email=new_email, username=new_username,
                    password=generate_password_hash(new_password,
                                                    method='sha256'))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html', form=form,
                           login=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login page contains a form for the user to login. The form is
    validated with the login form from forms.py. The details of the form
    is then queried in the user database to find the user with the
    username entered by the user. The password is then verified. If the
    user does not exist or the password is incorrect, we would flash an
    error message to the user. Otherwise, the user is authenticated and
    redirected to their personalised feed.

    :return: Redirects to feed page if user is authenticated, otherwise
             flash error messages.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        # Find the user
        user = User.query.filter_by(username=username).first()
        # Validate the user
        if user is None or not check_password_hash(user.password,
                                                   password):
            flash("Username or password incorrect.")
            return render_template('login.html', form=form,
                                   login=current_user.is_authenticated)
        # Create a session and redirect to feed
        login_user(user, remember=remember)
        return redirect(url_for('feed'))
    return render_template('login.html', form=form,
                           login=current_user.is_authenticated)


@app.route('/feed')
@login_required
def feed():
    """
    The feed page contains a personalised list of games that the current
    user has added to the list. It also shows other random games in the
    checkout section. This route can only be accessed if the current
    user is logged in.

    :return: Personalised feed of the current user
    """
    games = current_user.games
    random = Game.query.filter_by().order_by(func.random()).limit(5)
    return render_template('feed.html', user=current_user, games=games,
                           checkout=random,
                           login=current_user.is_authenticated)


@app.route('/add', methods=['POST'])
@login_required
def add():
    """
    A route to handle the response from AJAX to add a game to the user's
    game list. User must be logged in to access this page

    :return: json success code.
    """
    # Handling response from AJAX
    data = json.loads(request.data)
    response = data.get('response')
    index_token = response.find('_')
    game_id = int(response[index_token + 1:])
    # Find the game in the database
    game = Game.query.get(game_id)
    # Update user's game list
    if game not in current_user.games:
        current_user.games.append(game)
        db.session.add(current_user)
        db.session.commit()
    return json.dumps({'status': 'OK', 'response': game_id})


@app.route('/remove', methods=['POST'])
@login_required
def remove():
    """
    A route to handle the response from AJAX to remove a game from the
    user's game list. User must be logged in to access this page.

    :return: json success code.
    """
    # Handling response from AJAX
    data = json.loads(request.data)
    response = data.get('response')
    index_token = response.find('_')
    game_id = int(response[index_token + 1:])
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
    The website has a header that contains a search query. Any search
    query performed by the user is posted to this route. A query is then
    made to the game database that is similar to the query. The search
    route is only available if the user uses the search query and not
    using a GET request.

    :return: Redirect to search page with games similar to search query.
             Otherwise, redirect to index page if accessed with GET.
    """
    if request.form.get("search") is not None:
        query = request.form.get("search")
        search_query = "%" + query + "%"
        games = Game.query.filter(Game.title.like(search_query)).limit(
            10).all()
        return render_template('search.html', query=query, games=games,
                               login=current_user.is_authenticated)
    return redirect(url_for("index"))


@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    """
    The settings page allows a user to change their password. The page
    contains a form that for the user to change their password. The form
    is validated in forms.py. The old password is then verified with the
    password in the database. If they match, the password is then hashed
    and updated. If the password is incorrect, we would flash an error
    message for the user. Otherwise, we would flash a success message
    to the user.

    :return: A flash message to the user. Success if the password was
             updated, otherwise flash incorrect password.
    """
    form = PasswordForm()
    if form.validate_on_submit():
        old_password = request.form.get("old_password")
        if check_password_hash(current_user.password, old_password):
            new_password = request.form.get("password")
            current_user.password = generate_password_hash(new_password)
            # Update database
            db.session.add(current_user)
            db.session.commit()
            # Flash message
            flash("Password updated successfully.")
            return render_template('setting.html', form=form,
                                   login=current_user.is_authenticated)
        else:
            flash("Password incorrect.")
            return render_template('setting.html', form=form,
                                   login=current_user.is_authenticated)
    return render_template('setting.html', form=form,
                           login=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    """
    Logs the user out of the session.

    :return: Redirects to index page
    """
    logout_user()
    return redirect(url_for('index'))
