"""
This module contains the model for the app_request table
in the database.
"""

from db import db

class AppRequestModel(db.Model):
    """
    Class representing the app_requests table in the database.

    Attributes:
        id (int): The primary key of the appointment request.
        patient_id (int): The ID of the patient.
        date_and_time (int): The date and time of the appointment request.
        status (str): The status of the appointment request.
        app_responses (Relationship): The relationship to the AppResponseModel.
    """

    __tablename__ = "app_requests"

    id = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    patient = db.relationship("PatientModel", back_populates="app_requests")
    app_responses = db.relationship("AppResponseModel", back_populates="app_request", lazy="dynamic")
