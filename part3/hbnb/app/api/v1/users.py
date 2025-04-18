# app/api/v1/users.py

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

# API namespace for user operations
api = Namespace('users', description='User operations')

# user model for input validation and API documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user'),
    'is_admin': fields.Boolean(default=False, description='Admin status of the user')
})

# model for updates, all fields are optional
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='New password for the user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

# Users operations
@api.route('')
class UserList(Resource):
    # POST method to create a new user, requires JWT authentication
    @jwt_required()  # request must include a valid JWT token
    @api.expect(user_model, validate=True)  # validate input against user_model
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        # Check if the current user has admin privileges
        current_user = get_jwt_identity()  # Extracts user info from JWT token
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # Get the user data from the request payload
        user_data = api.payload
        
        # Check if the email is already in use
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Attempt to create the user via the facade
        try:
            new_user = facade.create_user(user_data)
            
            # Return only the ID and a success message (no password)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors
        
    # GET method to retrieve all users, requires JWT authentication and admin privileges
    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve a list of all users"""
        # Check if the current user has admin privileges
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # Fetch all users from the facade
        users = facade.get_all_users()
        if not users:
            return {'error': 'No users found'}, 404
        
        # Return the list of users as dictionaries
        return [user.to_dict() for user in users], 200

# operations on user by ID
@api.route('/<string:user_id>')
class UserResource(Resource):
    # GET method to retrieve user details, no authentication required
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        # Fetch user from facade
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Return the user data as a dictionary
        return user.to_dict(), 200
    
    # PUT method to update a user, requires JWT authentication
    @jwt_required()
    @api.expect(user_update_model, validate=True)  # Validates input against user_update_model
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action or Admin privileges required')
    def put(self, user_id):
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_data = api.payload
        
        # non-admin users can modify only their own data
        if not is_admin:
            if user_id != current_user['id']:
                return {'error': 'Unauthorized action'}, 403
            # Non-admins cannot change email or password
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        # Admins can modify any user's data, including email/password
        else:
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400
        
        # Fetch the user to update
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # update user via facade
        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any

    # DELETE a user, requires JWT authentication and admin privileges
    @jwt_required()
    @api.response(200, 'User deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user (admin only)"""
        # Get current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # only admin can delete
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        # Fetch the existing user
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Delete user via facade
        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
