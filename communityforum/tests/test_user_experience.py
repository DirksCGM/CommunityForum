import os
import unittest

from communityforum import app, db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LOGIN_DISABLED'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    # BASIC PAGE TESTS
    def test_home_page(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # USER REGISTRATION
    def register(self, username, email, password):
        return self.client.post(
            '/register',
            data=dict(username=username,
                      email=email,
                      password=password,
                      confirm_password=password),
            follow_redirects=True
        )

    # USER LOGIN
    def login(self, email, password):
        return self.client.post(
            '/login',
            data=dict(email=email,
                      password=password,
                      remember=True
                      ),
            follow_redirects=True
        )

    # COMMUNITY GENERATION
    def generate_new_community(self, title, description):
        return self.client.post(
            '/community/new',
            data=dict(title=title, description=description),
            follow_redirects=True
        )

    # POST GENERATION
    def generate_new_post(self, title, content, community):
        return self.client.post(
            '/post/new',
            data=dict(title=title, content=content, community=community, name='test user'),
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register('test user', 'testuser@test.com', 'testuser1234!')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_registration(self):
        response = self.register('test user', 'testusertest.com', 'testuser1234!')
        self.assertIn(b'Invalid email address.', response.data)

    def test_valid_login(self):
        response = self.login('testuser@test.com', 'testuser1234!')
        self.assertEqual(response.status_code, 200)

    def test_community_creation(self):
        with self.client:
            self.login('testuser@test.com', 'testuser1234!')
            # create community
            comm_response = self.generate_new_community('test community',
                                                        'this is a test community')
            self.assertEqual(comm_response.status_code, 200)

            # test community
            comm_test_response = self.client.get('/community/testcommunity')
            self.assertEqual(comm_test_response.status_code, 200)

    def test_post_creation(self):
        with self.client:
            self.login('testuser@test.com', 'testuser1234!')
            # create post
            post_response = self.generate_new_post('test post',
                                                   'this is a test post',
                                                   'testcommunity')
            self.assertEqual(post_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
