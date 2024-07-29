"""
Blueprint for handling appointment responses
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import AppResponseModel
from schemas import AppResponseSchema


blp = Blueprint(
    "appointment_responses",
    __name__,
    description="Operations on appointment responses"
)


@blp.route("/appointment_responses")
class AppointmentResponses(MethodView):
    """
    Class for handling requests to the /appointment_responses endpoint
    """
    @jwt_required()
    @blp.response(200, AppResponseSchema(many=True))
    def get(self):
        """
        Get all appointment responses in the database

        Returns:
            dict: A dictionary containing all appointment responses in
            the database
        """
        jwt = get_jwt()
        if jwt.get("role") == "admin":
            return AppResponseModel.query.all()
        else:
            return AppResponseModel.query.filter_by(therapist_id=jwt.get("sub")).all()

        abort(403, message="Admin/therapist privileges required to access resources")

    @jwt_required()
    @blp.arguments(AppResponseSchema)
    @blp.response(201, AppResponseSchema)
    def post(self, appointment_response_data):
        """
        Add a new appointment response to the database

        Args:
            appointment_response_data (dict): A dictionary containing the
            data for the new appointment response

        Returns:
            dict: A dictionary containing the newly created appointment response

        Raises:
            abort(400, message): If there is an error adding the appointment
            response to the database
        """
        jwt = get_jwt()
        if jwt.get("role") != "therapist":
            abort(403, message="Therapist privileges required to access resources")

        appointment_response = AppResponseModel(**appointment_response_data)
        try:
            db.session.add(appointment_response)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return appointment_response


@blp.route("/appointment_responses/<appointment_response_id>")
class AppointmentResponse(MethodView):
    """
    Class for handling requests to the
    /appointment_responses/<appointment_response_id> endpoint
    """
    @jwt_required()
    @blp.response(200, AppResponseSchema)
    def get(self, appointment_response_id):
        """
        Get an appointment response by ID

        Args:
            appointment_response_id (str): The ID of the appointment response
                to retrieve

        Returns:
            dict: A dictionary containing the requested appointment response

        Raises:
            NotFound: If the appointment response with the given ID does
            not exist
        """
        return AppResponseModel.query.get_or_404(appointment_response_id)

    @jwt_required()
    def delete(self, appointment_response_id):
        """
        Delete an appointment response by ID

        Args:
            appointment_response_id (str): The ID of the appointment response
            to delete

        Returns:
            dict: A dictionary containing a message indicating the success
            of the deletion

        Raises:
            NotFound: If the appointment response with the given ID does
            not exist
        """
        jwt = get_jwt()
        if jwt.get("role") != "therapist":
            abort(403, message="Therapist privilege required to do this action")

        appointment_response = AppResponseModel.query.get_or_404(appointment_response_id)
        db.session.delete(appointment_response)
        db.session.commit()
        return {"message": "Appointment response deleted successfully."}
