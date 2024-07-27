import unittest
from app import app, db
from models import User, Expense

class ExpenseTestCase(unittest.TestCase):
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

    def test_add_expense(self):
        with self.app.app_context():
            user = User(email='test@example.com', name='Test User', mobile='1234567890')
            db.session.add(user)
            db.session.commit()
        response = self.client.post('/expenses', json={
            'description': 'Dinner',
            'amount': 100.0,
            'date': '2024-07-27',
            'split_method': 'EQUAL',
            'splits': [{'user_id': user.id}],
            'user_id': user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dinner', response.get_data(as_text=True))

    def test_get_expenses(self):
        with self.app.app_context():
            user = User(email='test@example.com', name='Test User', mobile='1234567890')
            db.session.add(user)
            db.session.commit()
            expense = Expense(
                description='Dinner',
                amount=100.0,
                date='2024-07-27',
                split_method='EQUAL',
                splits=[{'user_id': user.id, 'amount': 100.0}],
                user_id=user.id
            )
            db.session.add(expense)
            db.session.commit()
        response = self.client.get(f'/expenses/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dinner', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
