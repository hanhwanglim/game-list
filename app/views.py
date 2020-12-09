from flask import render_template, request
from app import app
from app.forms import RegisterForm, LoginForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        print("hello")
        return "hello"
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("hello")
        return "hello"
    return render_template('login.html', form=form)