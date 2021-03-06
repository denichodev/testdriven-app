import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the user service."""

    def test_users(self):
        """Ensure the ping route behaves correctly"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'denicho',
                    'email': 'denichodev@gmail.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('denichodev@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure an error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure an error is thrown if the JSON object does not have username
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'denichodev@gmail.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown when email already exist."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'denicho',
                    'email': 'dneichodev@gmail.com'
                }),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'denicho2',
                    'email': 'dneichodev@gmail.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single users behaves correctly"""
        user = add_user('denicho', 'denichodev@gmail.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('denicho', data['data']['username'])
            self.assertIn('denichodev@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if no id is provided"""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if there is no user with the id."""
        with self.client:
            response = self.client.get('/users/123123')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behave correctly"""
        add_user('denicho', 'denichodev@gmail.com')
        add_user('denicho2', 'dencho.12@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('denicho', data['data']['users'][0]['username'])
            self.assertIn('denichodev@gmail.com', data[
                          'data']['users'][0]['email'])
            self.assertIn('denicho2', data['data']['users'][1]['username'])
            self.assertIn('dencho.12@gmail.com', data[
                          'data']['users'][1]['email'])
            self.assertEqual('success', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no
        users have been added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been added
        to the database."""
        add_user('dencho', 'dencho@gmail.com')
        add_user('ruth', 'ruthhtgl@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'dencho', response.data)
            self.assertIn(b'ruth', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the db."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='dencho', email='dencho@fake.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'dencho', response.data)


if __name__ == '__main__':
    unittest.main()
