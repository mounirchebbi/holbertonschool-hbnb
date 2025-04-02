# app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user'),
    'is_admin': fields.Boolean(default=False, description='Admin status of the user')
})

# Model for updates (all fields optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='New password for the user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_data = api.payload
        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            # Return only ID and success message, excluding password
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        current_user = get_jwt_identity()  # {'id': user_id, 'is_admin': bool}
        user = facade.get_user(user_id)    # user by id / current user by jwt
        if not user:
            return {'error': 'User not found'}, 404
        # Only allow users to see their own data or admins to see any data
        if current_user['id'] != user_id and not current_user['is_admin']:
            return {'error': 'Unauthorized access'}, 403
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Only allow users to update their own data or admins to update any data
        if current_user['id'] != user_id and not current_user['is_admin']:
            return {'error': 'Unauthorized access'}, 403
        # Prevent non-admins from changing is_admin status
        user_data = api.payload
        if 'is_admin' in user_data and not current_user['is_admin']:
            return {'error': 'Only admins can modify admin status'}, 403

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
