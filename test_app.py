import os
import unittest
from datetime import date

from app import app, db
from app.models import *
from werkzeug.security import check_password_hash

TEST_DB = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))


class Test(unittest.TestCase):
    def setUp(self):
        """
        Set config parameters to testing and creating a new test 
        database called test.db
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir,
                                                             TEST_DB)
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
        :return: A POST request to signup route
        """
        return self.app.post('/signup',
                             data=dict(email=email, username=username,
                                       password=password,
                                       confirm=password2,
                                       accept_tos=True),
                             follow_redirects=True)

    def login(self, username, password):
        """
        Simulates an entry by a user at the login page.
        :param username: Username of the user
        :param password: Password of the user
        :return: A POST request to login route
        """
        return self.app.post('/login', data=dict(username=username,
                                                 password=password,
                                                 remember=True),
                             follow_redirects=True)

    def test_sign_up(self):
        """
        Test the sign up functionality.

        Test included:
            Test if signup route is functional
            Test if a user can register
            Test if details of user are stored properly in the database
            Test if error messages are displayed accordingly
            Test if user already exist
        """
        # Test if route '/signup' is functional
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "Route is not functional")
        response = self.app.post('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "Route is not functional")

        # Test for first user
        response = self.register("adamadam@adammail.com", "adamadam",
                                 "adampassword", "adampassword")
        self.assertEqual(response.status_code, 200,
                         "User cannot register")

        user = User.query.filter_by(user_id=int(1)).first()
        self.assertEqual(user.email, "adamadam@adammail.com",
                         "Email not same")
        self.assertEqual(user.username, "adamadam", "Username not same")
        self.assertTrue(
            check_password_hash(user.password, "adampassword"),
            "Password not same")
        # Test for second user
        response = self.register("eveeve@evemail.com", "eveeve",
                                 "evepassword", "evepassword")
        self.assertEqual(response.status_code, 200,
                         "New user cannot register")

        user = User.query.filter_by(user_id=int(2)).first()
        self.assertEqual(user.email, "eveeve@evemail.com",
                         "Email not same")
        self.assertEqual(user.username, "eveeve", "Username not same")
        self.assertTrue(
            check_password_hash(user.password, "evepassword"),
            "Password not same")

        # Test invalid submission
        response = self.register('not_an_email', 'asdfasdf', 'password',
                                 'password')
        self.assertIn(b'Invalid email address.', response.data,
                      "Email validation failed")

        response = self.register('asdf@asdf.com', 'abc', 'password',
                                 'password')
        self.assertIn(
            b'Username must be between 4 and 25 characters long',
            response.data, "Username validation failed")

        response = self.register('asdf@asdf.com', 'asdfasdf',
                                 'password', 'PASSWORD')
        self.assertIn(b'Passwords must match', response.data,
                      "Password validation failed")

        # Test existing submission
        # Populating database
        user = User(email="user1@mail.com", username="user1",
                    password="password1")
        db.session.add(user)
        db.session.commit()
        response = self.register('user1@mail.com', 'user1', 'password1',
                                 'password1')
        self.assertIn(b'Username and email has already exist.',
                      response.data, "Flash message failed")
        response = self.register('user1@mail.com', 'newuser1',
                                 'password1', 'password1')
        self.assertIn(b'Email has already exist.', response.data,
                      "Flash message failed")
        response = self.register('newuser1@mail.com', 'user1',
                                 'password1', 'password1')
        self.assertIn(b'Username has already been taken.',
                      response.data, "Flash message failed")

    def test_login(self):
        """
        Test the login functionality.

        Test included:
            Test if login route is functional.
            Test if a user can login.
            Test if user is redirected to their feed.
            Test if for incorrect login details.
            Test if error messages are displayed.
        """
        # Test if route '/login' is functional
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "Route not functional")
        response = self.app.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "Route not functional")

        # Test for valid user
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        response = self.login("asdf", "asdfasdf")
        self.assertIn(b'Feed', response.data, "User is not redirected")

        # Test for invalid user
        self.register("asdf@mail.com", "USERX", "ASDFADSF", "ASDFASDF")
        response = self.login("userX", "asdfasdf")
        self.assertIn(b'Username or password incorrect.', response.data,
                      "Flash message failed")
        response = self.login("USERX", "asdfasdf")
        self.assertIn(b'Username or password incorrect.', response.data,
                      "Flash message failed")
        response = self.login("userX", "ASDFADSF")
        self.assertIn(b'Username or password incorrect.', response.data,
                      "Flash message failed")

    def test_feed(self):
        """
        Test the feed page.

        Test included:
            Test if the feed route is functional.
            Test redirect to login if user is not logged in.
            Test if user's game list is displayed on feed.
        """
        # Test if redirect to login page if no user is logged on
        response = self.app.get('/feed', follow_redirects=True)
        self.assertIn(b'Login', response.data,
                      "Redirect to login page failed")

        # Create games
        for i in range(5):
            game = Game(title="game" + str(i),
                        release_date=date(2020, 1, i + 1))
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
        self.assertIn(b'game0', response.data,
                      "Game is not available on feed")
        self.assertIn(b'game1', response.data,
                      "Game is not available on feed")
        self.assertIn(b'game2', response.data,
                      "Game is not available on feed")
        self.assertIn(b'game3', response.data,
                      "Game is not available on feed")
        self.assertIn(b'game4', response.data,
                      "Game is not available on feed")

    def test_search(self):
        """
        Test the search route and functionality.

        Tests included:
            Test redirect if user accesses using GET request.
            Test searched game is displayed on the page.
            Test not searched game is not displayed on the page.
        """
        # Test redirect to index if it is a GET request
        response = self.app.get('/search', follow_redirects=True)
        self.assertIn(b'<title>Game List</title>', response.data,
                      "Redirect to index failed")

        # Create games
        for i in range(3):
            game = Game(title="game" + str(i),
                        release_date=date(2020, 1, i + 1))
            db.session.add(game)
            db.session.commit()

        # Test if only the queried game is shown on the search page
        response = self.app.post('/search', data=dict(search="game0"),
                                 follow_redirects=True)
        self.assertIn(b'game0', response.data,
                      "Seached game not in page")
        self.assertNotIn(b'game1', response.data, "Wrong game in page")
        self.assertNotIn(b'game2', response.data, "Wrong game in page")

    def test_add(self):
        """
        Test the adding to list functionality.

        Test included:
            Test if the add route is functional.
            Test if game is added to the user's game list.
        """
        # Create user
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        # Create games
        for i in range(5):
            game = Game(title="game" + str(i),
                        release_date=date(2020, 1, i + 1))
            db.session.add(game)
            db.session.commit()
        # Login user
        self.login("asdf", "asdfasdf")
        # Simulating an AJAX response to the server
        response = self.app.post('/add', json={"response": "game_1"},
                                 follow_redirects=True)
        self.assertIn(b'{"status": "OK", "response": 1}', response.data,
                      "Response error")
        response = self.app.post('/add', json={"response": "game_2"},
                                 follow_redirects=True)
        self.assertIn(b'{"status": "OK", "response": 2}', response.data,
                      "Response error")
        # Check user's game list
        user = User.query.filter_by(user_id=int(1)).first()
        self.assertIn(user.games[0].title, "game0",
                      "Game not added to list")
        self.assertIn(user.games[1].title, "game1",
                      "Game not added to list")

    def test_remove(self):
        """
        Test the remove from list functionality.

        Test included:
            Test if the remove route is functional.
            Test if the game is removed from the user's game list.
        """
        # Create user
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        user = User.query.filter_by(user_id=int(1)).first()
        # Create games
        for i in range(5):
            game = Game(title="game" + str(i),
                        release_date=date(2020, 1, i + 1))
            db.session.add(game)
            db.session.commit()
        # Adding to user's game list
        for i in range(5):
            user.games.append(Game.query.get(i + 1))
            db.session.add(user)
            db.session.commit()
        # Login user
        self.login("asdf", "asdfasdf")
        # Simulating an AJAX response to the server
        response = self.app.post('/remove', json={"response": "game_1"},
                                 follow_redirects=True)
        self.assertIn(b'{"status": "OK", "response": 1}', response.data,
                      "Response error")
        # Check user's game list
        user = User.query.filter_by(user_id=int(1)).first()
        self.assertNotIn(user.games, ["game0"], "Game is not removed")

    def change_password(self, old_password, password, confirm):
        """
        Simulates an entry by the user at the setting page
        :param old_password: The current password of the user
        :param password: The new password 
        :param confirm: The repeated new password
        :return: A POST request to setting route
        """
        return self.app.post('/setting',
                             data=dict(old_password=old_password,
                                       password=password,
                                       confirm=confirm),
                             follow_redirects=True)

    def test_change_password(self):
        """
        Test the change password functionality.

        Test included:
            Test if the setting route is functional.
            Test if the password is validated.
            Test if error messages are displayed.
            Test if the password is updated in the database.
        """
        # Create a user and sign in
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        self.login("asdf", "asdfasdf")

        response = self.app.get('/setting', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "Route not functional")
        response = self.change_password("asdfasdf", "ASDFASDF", "asdfasdf")
        self.assertIn(b'Passwords must match.', response.data,
                      "Error message failed")
        response = self.change_password("ASDFADSF", "password",
                                        "password")
        self.assertIn(b'Password incorrect.', response.data,
                      "Error message failed")
        response = self.change_password("asdfasdf", "password",
                                        "password")
        self.assertIn(b'Password updated successfully.', response.data,
                      "Error message failed")

        user = User.query.filter_by(user_id=int(1)).first()
        self.assertTrue(check_password_hash(user.password, "password"),
                        "Password not same")

    def test_logout(self):
        """
        Test the functionality of the logout route.
        
        Test included:
            Test if the user can logout.
            Test if the user is redirected to the index page.
            Test if the user is able to access the restricted feed page.
        """
        # Create a user and sign in
        self.register("asdf@mail.com", "asdf", "asdfasdf", "asdfasdf")
        self.login("asdf", "asdfasdf")
        # Logout
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'<title>Game List</title>', response.data,
                      "User cannot logout")

        response = self.app.get('/feed', follow_redirects=True)
        self.assertIn(b'<title>Login</title>', response.data,
                      "User cannot logout")


if __name__ == "__main__":
    unittest.main()
