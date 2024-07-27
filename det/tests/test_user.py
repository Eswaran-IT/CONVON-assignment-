import unittest
from app import app, db
from models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_user(self):
        response = self.client.post('/users', json={
            'email': 'test@example.com',
            'name': 'Test User',
            'mobile': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@example.com', response.get_data(as_text=True))

    def test_get_user(self):
        with self.app.app_context():
            user = User(email='test@example.com', name='Test User', mobile='1234567890')
            db.session.add(user)
            db.session.commit()
        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@example.com', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
