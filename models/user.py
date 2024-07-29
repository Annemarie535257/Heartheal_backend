"""
This module contains the User model.
"""

from db import db

class UserModel(db.Model):
    """
    Represents a user in the system.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) # Add username field
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient')  # Add role field

    def __init__(self, username, first_name, last_name, email, password, role='patient'):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    patient = db.relationship("PatientModel", back_populates="user", uselist=False)
    therapist = db.relationship("TherapistModel", back_populates="user", uselist=False)
    admin = db.relationship("AdminModel", back_populates="user", uselist=False)
