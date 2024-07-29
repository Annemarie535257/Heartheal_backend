"""
This module contains the model for the therapist table in the database.
"""

from db import db

class TherapistModel(db.Model):
    """
    Class representing the therapist table in the database.

    Attributes:
        id (int): The primary key of the therapist.
        license_no (int): The license number.
        specialization (str): The specialization of the therapist.
        years_of_experience (int): The years of experience.
        bio (str): The biography of the therapist.
        app_responses (Relationship): The appointments response
        associated with the therapists.
    """

    __tablename__ = "therapists"

    id = db.Column(db.Integer, primary_key=True)
    license_no = db.Column(db.Integer, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(500), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="therapist")
    app_responses = db.relationship("AppResponseModel", back_populates="therapist", lazy="dynamic")
