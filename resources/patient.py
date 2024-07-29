"""
Blueprint for patient resources
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import PatientModel
from schemas import PatientSchema

blp = Blueprint(
    "patients",
    __name__,
    description="Operations on patients"
)

@blp.route("/patients")
class Patients(MethodView):
    """
    Class for handling requests to the /patients endpoint
    """
    @jwt_required()
    @blp.response(200, PatientSchema(many=True))
    def get(self):
        """
        Get all patients in the database

        Returns:
            dict: A dictionary containing all patients in the database
        """
        jwt = get_jwt()
        if jwt.get("role") == "admin":
            return PatientModel.query.all()
        abort(403, message="Admin privileges required to access resources")

    @jwt_required()
    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    def post(self, patient_data):
        """
        Add a new patient to the database

        Args:
            patient_data (dict): A dictionary containing the data for the
            new patient

        Returns:
            tuple: A tuple containing the newly added patient and the
            HTTP status code 201

        Raises:
            abort: If there is an error adding the patient to the database
        """
        jwt = get_jwt()
        user_id = jwt.get("sub")

        patient = PatientModel(**patient_data, user_id=user_id)

        try:
            db.session.add(patient)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return patient

@blp.route("/patients/<patient_id>")
class Patient(MethodView):
    """
    Class for handling requests to the /patients/<patient_id> endpoint
    """
    @jwt_required()
    @blp.response(200, PatientSchema)
    def get(self, patient_id):
        """
        Get a patient by ID

        Args:
            patient_id (str): The ID of the patient to retrieve

        Returns:
            tuple: A tuple containing the requested patient and the
            HTTP status code 200

        Raises:
            404: If the patient with the given ID is not found
        """
        jwt = get_jwt()
        user_role = jwt.get("role")

        if user_role == "admin":
            return PatientModel.query.get_or_404(patient_id)
        abort(403, message="Admin privileges required to access resources")

    @jwt_required()
    def delete(self, patient_id):
        """
        Delete a patient by ID

        Args:
            patient_id (str): The ID of the patient to delete

        Returns:
            tuple: A tuple containing a message indicating the deletion and
            the HTTP status code 200

        Raises:
            404: If the patient with the given ID is not found
        """
        jwt = get_jwt()
        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to delete a patient")

        patient = PatientModel.query.get_or_404(patient_id)

        db.session.delete(patient)
        db.session.commit()

        return {"message": "Patient deleted"}, 200
