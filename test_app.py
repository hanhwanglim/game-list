import os
import unittest
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db
from app.models import *
from flask_login import current_user

TEST_DB = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))


class BasicTests(unittest.TestCase):
    def setUp(self):
        """
        Set config parameters to testing and creating a new test database called test.db
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        """
        Reinitialize test database
        """
        db.drop_all()

    def register(self, email, username, password, password2):
        """
        Simulates an entry by a user at the sign up page.
        :param email: Email of the user
        :param username: Username of the user
        :param password: Password of the user
        :param password2: Confirm password for the user
        """
        return self.app.post('/signup', data=dict(email=email, username=username, password=password, confirm=password2, accept_tos=True), follow_redirects=True)

    def login(self, username, password):
        """
        Simulates an entry by a user at the login page.
        :param username: Username of the user
        :param password: Password of the user
        """
        return self.app.post('/login', data=dict(username=username, password=password, remember=True), follow_redirects=True)

    def test_sign_up(self):
        # Test if route '/signup' is functional
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Test for first user
        response = self.register("adamadam@adammail.com", "adamadam", "adampassword", "adampassword")
        self.assertEqual(response.status_code, 200)
        
        user = User.query.filter_by(user_id=int(1)).first()
        self.assertEqual(user.email, "adamadam@adammail.com", "Email not same")
        self.assertEqual(user.username, "adamadam", "Username not same")
        self.assertTrue(check_password_hash(user.password, "adampassword"), "Password not same")
        # Test for second user
        response = self.register("eveeve@evemail.com", "eveeve", "evepassword", "evepassword")
        self.assertEqual(response.status_code, 200)
        
        user = User.query.filter_by(user_id=int(2)).first()
        self.assertEqual(user.email, "eveeve@evemail.com", "Email not same")
        self.assertEqual(user.username, "eveeve", "Username not same")
        self.assertTrue(check_password_hash(user.password, "evepassword"), "Password not same")

        # Test invalid submission
        response = self.register('not_an_email', 'asdfasdf', 'password', 'password')
        self.assertIn(b'Invalid email address.', response.data)

        response = self.register('asdf@asdf.com', 'abc', 'password', 'password')
        self.assertIn(b'Username must be between 4 and 25 characters long.', response.data)

        response = self.register('asdf@asdf.com', 'asdfasdf', 'password', 'PASSWORD')
        self.assertIn(b'Passwords must match.', response.data)

        # Test existing submission
        # Populating database
        user = User(email="user1@mail.com", username="user1", password="password1")
        db.session.add(user)
        db.session.commit()
        response = self.register('user1@mail.com', 'user1', 'password1', 'password1')
        self.assertIn(b'Username and email has already exist.', response.data)
        response = self.register('user1@mail.com', 'newuser1', 'password1', 'password1')
        self.assertIn(b'Email has already exist.', response.data)
        response = self.register('newuser1@mail.com', 'user1', 'password1', 'password1')
        self.assertIn(b'Username has already been taken.', response.data)
    
    def test_login(self):
        # Test if route '/login' is functional
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Test for valid user
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        response = self.login("asdf", "asdfasdf")
        self.assertIn(b'Feed', response.data)

        # Test for invalid user
        self.register("asdf@mail.com", "USERX", "ASDFADSF", "ASDFASDF")
        response = self.login("userX", "asdfasdf")
        self.assertIn(b'Username or password incorrect.', response.data)
        response = self.login("USERX", "asdfasdf")
        self.assertIn(b'Username or password incorrect.', response.data)
        response = self.login("userX", "ASDFADSF")
        self.assertIn(b'Username or password incorrect.', response.data)

    def test_feed(self):
        # Test if redirect to login page if no user is logged on
        response = self.app.get('/feed', follow_redirects=True)
        self.assertIn(b'Login', response.data)

        # Create games
        for i in range(5):
            game = Game(title="game" + str(i), release_date=date(2020, 1, i+1))
            db.session.add(game)
            db.session.commit()
        
        # Create user
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        user = User.query.filter_by(user_id=int(1)).first()
        # Adding to user's game list
        for i in range(5):
            user.games.append(Game.query.get(i + 1))
            db.session.add(user)
            db.session.commit()
        
        # Check if game list is available on user's feed
        response = self.login("asdf", "asdfasdf")
        self.assertIn(b'game0', response.data)
        self.assertIn(b'game1', response.data)
        self.assertIn(b'game2', response.data)
        self.assertIn(b'game3', response.data)
        self.assertIn(b'game4', response.data)

    def test_search(self):
        # Create games
        for i in range(3):
            game = Game(title="game" + str(i), release_date=date(2020, 1, i+1))
            db.session.add(game)
            db.session.commit()

        # Test if only the queried game is shown on the search page
        response = self.app.post('/search', data=dict(search="game0"), follow_redirects=True)
        self.assertIn(b'game0', response.data)
        self.assertNotIn(b'game1', response.data)
        self.assertNotIn(b'game2', response.data)


if __name__ == "__main__":
    unittest.main()
