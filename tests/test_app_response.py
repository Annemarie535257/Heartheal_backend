import unittest
from models.user import UserModel
from models.therapist import TherapistModel
from models.patient import PatientModel
from models.app_request import AppRequestModel
from models.app_response import AppResponseModel
from db import db
from flask import Flask

class AppResponseModelTestCase(unittest.TestCase):
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

    def test_create_app_response(self):
        """
        Test app response creation and attribute assignment.
        """
        # Create user, therapist, and patient
        user_therapist = UserModel(
            username="umutoniange",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1@gmail.com",
            password="password123",
            role="therapist"
        )
        db.session.add(user_therapist)
        db.session.commit()

        therapist = TherapistModel(
            license_no=123456,
            specialization="Clinical Psychology",
            years_of_experience=10,
            bio="Experienced clinical psychologist with over a decade of practice.",
            user_id=user_therapist.id
        )
        db.session.add(therapist)
        db.session.commit()

        user_patient = UserModel(
            username="umutoniange2",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1+1@gmail.com",
            password="password123",
            role="patient"
        )
        db.session.add(user_patient)
        db.session.commit()

        patient = PatientModel(
            age=30,
            gender="Male",
            contact_no=1234567890,
            address="123 Main St",
            user_id=user_patient.id
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

        # Create appointment response
        app_response = AppResponseModel(
            therapist_id=therapist.id,
            date=1627929600000,  # Example timestamp
            app_request_id=app_request.id
        )
        db.session.add(app_response)
        db.session.commit()

        # Retrieve the app response from the database
        retrieved_app_response = AppResponseModel.query.filter_by(id=app_response.id).first()
        
        self.assertIsNotNone(retrieved_app_response)
        self.assertEqual(retrieved_app_response.therapist_id, therapist.id)
        self.assertEqual(retrieved_app_response.date, 1627929600000)
        self.assertEqual(retrieved_app_response.app_request_id, app_request.id)

    def test_app_response_relationships(self):
        """
        Test the relationships of app response with therapist and appointment request.
        """
        # Create user, therapist, and patient
        user_

