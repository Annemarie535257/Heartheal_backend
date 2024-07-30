import unittest
from models.user import UserModel
from models.patient import PatientModel
from models.app_request import AppRequestModel
from db import db
from flask import Flask

class AppRequestModelTestCase(unittest.TestCase):
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

    def test_create_app_request(self):
        """
        Test app request creation and attribute assignment.
        """
        # Create user and patient
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

        # Create appointment request
        app_request = AppRequestModel(
            patient_id=patient.id,
            date_and_time=1627843200000,  # Example timestamp
            status="pending"
        )
        db.session.add(app_request)
        db.session.commit()

        # Retrieve the app request from the database
        retrieved_app_request = AppRequestModel.query.filter_by(id=app_request.id).first()
        
        self.assertIsNotNone(retrieved_app_request)
        self.assertEqual(retrieved_app_request.patient_id, patient.id)
        self.assertEqual(retrieved_app_request.date_and_time, 1627843200000)
        self.assertEqual(retrieved_app_request.status, "pending")

    def test_app_request_relationships(self):
        """
        Test the relationships of app request with patient.
        """
        # Create user and patient
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

        # Create appointment request
        app_request = AppRequestModel(
            patient_id=patient.id,
            date_and_time=1627843200000,  # Example timestamp
            status="pending"
        )
        db.session.add(app_request)
        db.session.commit()

        # Retrieve the app request from the database
        retrieved_app_request = AppRequestModel.query.filter_by(id=app_request.id).first()
        
        self.assertIsNotNone(retrieved_app_request)
        self.assertEqual(retrieved_app_request.patient_id, patient.id)
        self.assertEqual(retrieved_app_request.date_and_time, 1627843200000)
        self.assertEqual(retrieved_app_request.status, "pending")
        self.assertEqual(retrieved_app_request.patient.id, patient.id)

if __name__ == '__main__':
    unittest.main()

