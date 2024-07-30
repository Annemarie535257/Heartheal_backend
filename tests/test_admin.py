import unittest
from models.user import UserModel
from models.admin import AdminModel
from db import db
from flask import Flask

class AdminModelTestCase(unittest.TestCase):
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

    def test_create_admin(self):
        """
        Test admin creation and attribute assignment.
        """
        # Create user
        user = UserModel(
            username="umutoniange",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1@gmail.com",
            password="password123",
            role="admin"
        )
        db.session.add(user)
        db.session.commit()

        # Create admin
        admin = AdminModel(
            user_id=user.id
        )
        db.session.add(admin)
        db.session.commit()

        # Retrieve the admin from the database
        retrieved_admin = AdminModel.query.filter_by(id=admin.id).first()
        
        self.assertIsNotNone(retrieved_admin)
        self.assertEqual(retrieved_admin.user_id, user.id)

    def test_admin_relationships(self):
        """
        Test the relationships of admin with user.
        """
        # Create user
        user = UserModel(
            username="umutoniange",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1@gmail.com",
            password="password123",
            role="admin"
        )
        db.session.add(user)
        db.session.commit()

        # Create admin
        admin = AdminModel(
            user_id=user.id
        )
        db.session.add(admin)
        db.session.commit()

        # Retrieve the admin from the database
        retrieved_admin = AdminModel.query.filter_by(id=admin.id).first()
        
        self.assertIsNotNone(retrieved_admin)
        self.assertEqual(retrieved_admin.user_id, user.id)
        self.assertEqual(retrieved_admin.user.id, user.id)

if __name__ == '__main__':
    unittest.main()

