# app/api/v1/amenities.py

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the API namespace for amenity-related operations
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for creation and API documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, default='', description='Description of the amenity')
})

# Define a separate model for updates, where all fields are optional
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

# Resource for handling operations on the collection of amenities
@api.route('')
class AmenityList(Resource):
    # POST method to create a new amenity, requires JWT authentication and admin privileges
    @jwt_required()  # Ensures the request includes a valid JWT token
    @api.expect(amenity_model, validate=True)  # Validates input against amenity_model
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        
        # Restrict amenity creation to admin users only
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # Get the amenity data from the request payload
        amenity_data = api.payload
        
        # Attempt to create the amenity via the facade
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any
    
    # GET method to retrieve all amenities, no authentication required
    @api.response(200, 'List of amenities retrieved')
    def get(self):
        # Fetch all amenities from the facade
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

# Resource for handling operations on a specific amenity by ID
@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    # GET method to retrieve amenity details, no authentication required
    @api.response(200, 'Amenity details retrieved')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        # Fetch the amenity from the facade
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    # PUT method to update an amenity, requires JWT authentication and admin privileges
    @jwt_required()
    @api.expect(amenity_update_model, validate=True)  # Validates input against amenity_update_model
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        
        # Restrict amenity updates to admin users only
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # Get the amenity data from the request payload
        amenity_data = api.payload
        
        # Fetch the existing amenity
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Attempt to update the amenity via the facade
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any

    # DELETE method to remove an amenity, requires JWT authentication and admin privileges
    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        
        # Restrict deletion to admin users only
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # Fetch the existing amenity
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Delete the amenity via the facade
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200
