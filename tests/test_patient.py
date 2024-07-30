import unittest
from models.user import UserModel
from models.patient import PatientModel
from db import db
from flask import Flask

class PatientModelTestCase(unittest.TestCase):
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

    def test_create_patient(self):
        """
        Test patient creation and attribute assignment.
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

        patient = PatientModel(
            age=30,
            gender="Male",
            contact_no=1234567890,
            address="123 Main St",
            user_id=user.id
        )
        db.session.add(patient)
        db.session.commit()

        retrieved_patient = PatientModel.query.filter_by(user_id=user.id).first()
        
        self.assertIsNotNone(retrieved_patient)
        self.assertEqual(retrieved_patient.age, 30)
        self.assertEqual(retrieved_patient.gender, "Male")
        self.assertEqual(retrieved_patient.contact_no, 1234567890)
        self.assertEqual(retrieved_patient.address, "123 Main St")

if __name__ == '__main__':
    unittest.main()

