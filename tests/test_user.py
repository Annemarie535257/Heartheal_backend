import unittest
from models.user import UserModel
from db import db
from flask import Flask

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Create a new app context and initialize the database before each test.
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        """
        Remove the app context after each test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """
        Test user creation and attribute assignment.
        """
        user = UserModel(
            username="umutoniange",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1@gmail.com",
            password="password123",
            role="patient"
        )
        db.session.add(user)
        db.session.commit()

        retrieved_user = UserModel.query.filter_by(email="umutange1@gmail.com").first()
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "umutoniange")
        self.assertEqual(retrieved_user.first_name, "Ange")
        self.assertEqual(retrieved_user.last_name, "Umutoni")
        self.assertEqual(retrieved_user.email, "umutange1@gmail.com")
        self.assertEqual(retrieved_user.role, "patient")

if __name__ == '__main__':
    unittest.main()

