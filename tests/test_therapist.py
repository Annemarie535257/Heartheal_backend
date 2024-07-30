import unittest
from models.user import UserModel
from models.therapist import TherapistModel
from db import db
from flask import Flask

class TherapistModelTestCase(unittest.TestCase):
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

    def test_create_therapist(self):
        """
        Test therapist creation and attribute assignment.
        """
        user = UserModel(
            username="umutoniange",
            first_name="Ange",
            last_name="Umutoni",
            email="umutange1@gmail.com",
            password="password123",
            role="therapist"
        )
        db.session.add(user)
        db.session.commit()

        therapist = TherapistModel(
            license_no=123456,
            specialization="Clinical Psychology",
            years_of_experience=10,
            bio="Experienced clinical psychologist with over a decade of practice.",
            user_id=user.id
        )
        db.session.add(therapist)
        db.session.commit()

        retrieved_therapist = TherapistModel.query.filter_by(user_id=user.id).first()
        
        self.assertIsNotNone(retrieved_therapist)
        self.assertEqual(retrieved_therapist.license_no, 123456)
        self.assertEqual(retrieved_therapist.specialization, "Clinical Psychology")
        self.assertEqual(retrieved_therapist.years_of_experience, 10)
        self.assertEqual(retrieved_therapist.bio, "Experienced clinical psychologist with over a decade of practice.")

if __name__ == '__main__':
    unittest.main()

