"""
This module contains the Admin model
"""

from db import db

class AdminModel(db.Model):
    """
    This class represents an admins table in the database.
    """

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    user = db.relationship("UserModel", back_populates="admin")
