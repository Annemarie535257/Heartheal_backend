"""
This module contains the model for the app_response table
in the database.
"""

from db import db

class AppResponseModel(db.Model):
    """
    Class representing the app_responses table in the database.

    Attributes:
        id (int): The primary key of the appointment response.
        therapist_id (int): The ID of the therapist.
        date (int): The date of the appointment response.
        app_request_id (int): The foreign key referencing the app_requests table.
        app_request (Relationship): The relationship to the AppRequestModel.
    """

    __tablename__ = "app_responses"

    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey("therapists.id"), nullable=False)
    date = db.Column(db.BigInteger, nullable=False)
    app_request_id = db.Column(db.Integer, db.ForeignKey("app_requests.id"), nullable=False)

    therapist = db.relationship("TherapistModel", back_populates="app_responses")
    app_request = db.relationship("AppRequestModel", back_populates="app_responses")
