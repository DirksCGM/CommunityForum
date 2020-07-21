import os
import unittest

from communityforum import app, db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    # BASIC PAGE TESTS
    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # USER AUTHENTICATION
    def register(self, username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username,
                      email=email,
                      password=password,
                      confirm_password=password,
                      follow_redirects=True)
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email,
                      password=password,
                      follow_redirects=True)
        )

    def test_valid_user_registration(self):
        response = self.register('test user', 'testuser@testuser.com', 'testuser1234!')
        self.assertEqual(response.status_code, 302)

    def test_invalid_user_registration(self):
        response = self.register('test user', 'testusertestuser.com', 'testuser1234!')
        self.assertIn(b'Invalid email address.', response.data)

    def test_valid_login(self):
        response = self.login('testuser@testuser.com', 'testuser1234!')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
