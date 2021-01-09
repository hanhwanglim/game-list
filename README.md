# Game List
Game List is a web application that allows users to have a personalised record of the games they have played.

## Installation
```bash
module add anaconda3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## Usage
```bash
export FLASK_APP=run.py
flask run
```

## Admin page
To access the admin page go to the [login](http://localhost:5000/login/) page.

Use the credentials:
```
Username: admin
Password: password
```
Then go to the [admin](http://localhost:5000/admin/) page.

## Testing
```bash
coverage run test_app.py
coverage report -m app/*.py
```