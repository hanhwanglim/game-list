from flask import render_template, request
from app import app
from app.forms import RegisterForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("hello")
        return "hello"
    return render_template('signup.html', form=form)

