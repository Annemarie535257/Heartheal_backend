from marshmallow import Schema, fields, validate# type: ignore

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True, validate=lambda x: x in ["patient", "therapist"])

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    Age = fields.Int(required=True)
    gender = fields.Str(required=True)
    contact_no = fields.Str(required=True)
    address = fields.Str(required=True)
    user_id = fields.Int(required=True)

class TherapistSchema(Schema):
    id = fields.Int(dump_only=True)
    license_no = fields.Str(required=True)
    specialization = fields.Str(required=True)
    years_of_experience = fields.Int(required=True)
    bio = fields.Str(required=True)
    user_id = fields.Int(required=True)

class AppRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    date_and_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    status = fields.Str(required=True)

class AppResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    therapist_id = fields.Int(required=True)
    date = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    response = fields.Str(required=True)
