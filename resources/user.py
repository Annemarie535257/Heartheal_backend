"""
This module contains the User blueprint.
"""

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from db import db
from models import UserModel
from schemas import UserSchema
from flask import jsonify
from flask import render_template

blp = Blueprint(
    "users",
    __name__,
    description="Operations on users"
)

# @blp.route("/")
# class Home(MethodView):
#     def get(self):
#         return render_template("index.html")
    
# @blp.route('/about')
# def about():
#     return render_template('about.html')

# @blp.route('/services')
# def services():
#     return render_template('services.html')

# @blp.route('/contact')
# def contact():
#     return render_template('contact.html')

# @blp.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# @blp.route('/consult')
# def consult():
#     return render_template('consult.html')

# @blp.route('/meditation')
# def meditation():
#     return render_template('midt.html')

# @blp.route('/mindfulness')
# def mindfulness():
#     return render_template('mindfulness.html')

# @blp.route('/groups')
# def groups():
#     return render_template('groups.html')

# @blp.route('/settings')
# def settings():
#     return render_template('settings.html')

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Register a new user

        Parameters:
        - user_data (dict): The data of the user to be registered.
        It should contain the following keys:
            - first_name (str): The first name of the user.
            - last_name (str): The last name of the user.
            - email (str): The email of the user.
            - password (str): The password of the user.
            - role (str): The role of the user. Can be 'patient' or 'therapist'.

        Returns:
        - dict: A dictionary containing the message.

        Raises:
        - 409 Conflict: If a user with the same email already exists.
        """
        # Check if user already exists (using username now)
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        hashed_password = pbkdf2_sha256.hash(user_data["password"])
        user_data["password"] = hashed_password

        # Create the user
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully."}),201
    
        if UserModel.query.filter_by(email=user_data["email"]).first():
            abort(409, message="User already exists")

        user = UserModel(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema(only=("email", "password")))
    def post(self, user_data):
        """
        Log in a user

        Parameters:
        - user_data (dict): The data of the user to be logged in.
        It should contain the following keys:
            - email (str): The email of the user.
            - password (str): The password of the user.

        Returns:
        - dict: A dictionary containing the message and the access token.

        Raises:
        - 401 Unauthorized: If the email or password is incorrect.
        """
        user = UserModel.query.filter_by(email=user_data["email"]).first()
        password = user_data["password"]
        if user is None or not pbkdf2_sha256.verify(password, user.password):
            abort(401, message="Incorrect email or password")

        access_token = create_access_token(identity=user.id)

        # Check the role of the user (adjust based on your app logic)
        role = "user"  # Example role assignment

        return {
            "message": "Logged in successfully",
            "access_token": access_token,
            "role": user.role
        }

@blp.route("/users/<user_id>")
class User(MethodView):
    """
    Class for handling requests to the /users/<user_id> endpoint
    """
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Get a user by ID

        Parameters:
        - user_id (int): The ID of the user to retrieve.

        Returns:
        - UserModel: The user object corresponding to the given ID.

        Raises:
        - 404 Not Found: If no user with the given ID exists.
        """
        return UserModel.query.get_or_404(user_id)

    @jwt_required()
    def delete(self, user_id):
        """
        Delete a user by ID

        Parameters:
        - user_id (int): The ID of the user to delete.

        Returns:
        - dict: A dictionary containing the message.

        Raises:
        - 403 Forbidden: If the user does not have admin privileges.
        - 404 Not Found: If no user with the given ID exists.
        """
        jwt = get_jwt()

        if jwt.get("role") == "admin":
            user = UserModel.query.get(user_id)
            if user is None:
                abort(404, message="User not found")

            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}

        abort(403, message="Admin privileges required to carry out this action")
