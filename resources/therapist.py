"""
Blueprint for therapist resources
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import TherapistModel
from schemas import TherapistSchema

blp = Blueprint(
    "therapists",
    __name__,
    description="Operations on therapists"
)

@blp.route("/therapists")
class Therapists(MethodView):
    """
    Class for handling requests to the /therapists endpoint
    """
    @jwt_required()
    @blp.response(200, TherapistSchema(many=True))
    def get(self):
        """
        Get all therapists in the database

        Returns:
            dict: A dictionary containing all therapists in the database
        """
        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to access resources")
        return TherapistModel.query.all()

    @jwt_required()
    @blp.arguments(TherapistSchema)
    @blp.response(201, TherapistSchema)
    def post(self, therapist_data):
        """
        Add a new therapist to the database.

        Args:
            therapist_data (dict): A dictionary containing the data
            for the new therapist.

        Returns:
            tuple: A tuple containing the newly added therapist and the
            HTTP status code 201.

        Raises:
            abort: If there is an error adding the therapist to the database.
        """
        jwt = get_jwt()
        user_id = jwt.get("sub")

        therapist = TherapistModel(**therapist_data, user_id=user_id)

        try:
            db.session.add(therapist)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return therapist


@blp.route("/therapists/<therapist_id>")
class Therapist(MethodView):
    """
    Class for handling requests to the /therapists/<therapist_id> endpoint
    """
    @jwt_required()
    @blp.response(200, TherapistSchema)
    def get(self, therapist_id):
        """
        Get a therapist by ID

        Args:
            therapist_id (str): The ID of the therapist to retrieve

        Returns:
            tuple: A tuple containing the requested therapist and the
            HTTP status code 200

        Raises:
            404: If the therapist with the given ID is not found
        """
        jwt = get_jwt()
        user_role = jwt.get("role")
        if user_role == "admin":
            return TherapistModel.query.get_or_404(therapist_id)
        abort(403, message="Admin privileges required to access resources")

    @jwt_required()
    def delete(self, therapist_id):
        """
        Delete a therapist by ID

        Args:
            therapist_id (str): The ID of the therapist to delete

        Returns:
            dict: A dictionary containing a message indicating the therapist
            was deleted

        Raises:
            404: If the therapist with the given ID is not found
        """
        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to delete a therapist")

        therapist = TherapistModel.query.get_or_404(therapist_id)
        db.session.delete(therapist)
        db.session.commit()
        return {"message": "Therapist deleted"}
