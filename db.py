"""
This module initializes the SQLAlchemy object for the Flask application.

Attributes:
    db (SQLAlchemy): The SQLAlchemy object used for database operations.
"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()