"""
Blueprint for handling appointment requests
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import AppRequestModel
from schemas import AppRequestSchema


blp = Blueprint(
    "app_requests",
    __name__,
    description="Operations on appointment requests"
)


@blp.route("/appointment_requests")
class AppointmentRequests(MethodView):
    """
    Class for handling requests to the /appointment_requests endpoint
    """
    @jwt_required()
    @blp.response(200, AppRequestSchema(many=True))
    def get(self):
        """
        Get all appointment requests in the database

        Returns:
            dict: A dictionary containing all appointment requests in
            the database
        """
        jwt = get_jwt()
        if jwt.get("role") == "admin":
            return AppRequestModel.query.all()
        else:
            return AppRequestModel.query.filter_by(patient_id=jwt.get("sub")).all()

        abort(403, message="Admin/household privileges required to access resources")

    @jwt_required()
    @blp.arguments(AppRequestSchema)
    @blp.response(201, AppRequestSchema)
    def post(self, appointment_request_data):
        """
        Add a new appointment request to the database

        Args:
            appointment_request_data (dict): A dictionary containing the
            data for the new appointment request

        Returns:
            dict: A dictionary containing the newly created appointment request

        Raises:
            abort(400, message): If there is an error adding the appointment
            request to the database
        """
        jwt = get_jwt()
        if jwt.get("role") != "patient":
            abort(403, message="Patient privileges required to access resources")

        appointment_request = AppRequestModel(**appointment_request_data)
        try:
            db.session.add(appointment_request)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return appointment_request


@blp.route("/appointment_requests/<appointment_request_id>")
class AppointmentRequest(MethodView):
    """
    Class for handling requests to the
    /appointment_requests/<appointment_request_id> endpoint
    """
    @jwt_required()
    @blp.response(200, AppRequestSchema)
    def get(self, appointment_request_id):
        """
        Get an appointment request by ID

        Args:
            appointment_request_id (str): The ID of the appointment request
                to retrieve

        Returns:
            dict: A dictionary containing the requested appointment request

        Raises:
            NotFound: If the appointment request with the given ID does
            not exist
        """
        return AppRequestModel.query.get_or_404(appointment_request_id)

    @jwt_required()
    def delete(self, appointment_request_id):
        """
        Delete an appointment request by ID

        Args:
            appointment_request_id (str): The ID of the appointment request
            to delete

        Returns:
            dict: A dictionary containing a message indicating the success
            of the deletion

        Raises:
            NotFound: If the appointment request with the given ID does
            not exist
        """
        jwt = get_jwt()
        if jwt.get("role") != "patient":
            abort(403, message="Patient privilege required to do this action")

        appointment_request = AppRequestModel.query.get_or_404(appointment_request_id)
        db.session.delete(appointment_request)
        db.session.commit()
        return {"message": "Appointment request deleted successfully."}
