"""
This module contains the model for the patient table in the database.
"""

from db import db

class PatientModel(db.Model):
    """
    Class representing the patient table in the database.

    Attributes:
        id (int): The primary key of the patient.
        age (int): The age of the patient.
        gender (str): The gender of the patient.
        contact_no (int): The telephone number.
        address (str): The area where the household is located.
        app_requests (Relationship): The appointment requests
        associated with the patients.
    """

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    contact_no = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    user = db.relationship("UserModel", back_populates="patient")
    app_requests = db.relationship("AppRequestModel", back_populates="patient", lazy="dynamic")
