# app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app

# API namespace for place operations
api = Namespace('places', description='Place operations')

# amenity model to enrich place data in responses
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# place model for input validation and API documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# places operations
@api.route('')
class PlaceList(Resource):
    # POST create a new place, requires JWT authentication
    @jwt_required()  # Ensures the request includes a valid JWT token
    @api.expect(place_model)  # Validates input against place_model
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place_data = api.payload
        
        # non-admin can create places only for themselves
        if not is_admin and place_data['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        # Admins can assign any owner, but must verify the owner exists
        if is_admin and not facade.get_user(place_data['owner_id']):
            return {'error': 'Owner not found'}, 400
        
        # create the place via facade
        try:
            new_place = facade.create_place(place_data)
            return self._enrich_place_data(new_place), 201  # Return enriched data
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any
    
    # GET method to retrieve all places, no authentication required
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Fetch all places from the facade
        places = facade.get_all_places()
        # Enrich each place with owner and amenity details
        return [self._enrich_place_data(place) for place in places], 200
    
    # Helper method to include additional data in place responses
    def _enrich_place_data(self, place):
        """Helper method to include owner and amenities details in the response."""
        # Fetch the owner of the place
        owner = facade.get_user(place.owner_id)
        
        # Extract amenity IDs from the dynamic relationship and fetch each Amenity
        amenity_ids = [amenity.id for amenity in place.amenities.all()]  # Use .all() to get the list
        amenities = [facade.get_amenity(amenity_id) for amenity_id in amenity_ids]
        
        # Build the enriched place dictionary
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict() if owner else None
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities if amenity]
        return place_dict

# place by ID operations
@api.route('/<place_id>')
class PlaceResource(Resource):
    # GET method to retrieve place details, no authentication required
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Fetch the place from the facade
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Return enriched place data
        return self._enrich_place_data(place), 200
    
    # PUT method to update a place, requires JWT authentication
    @jwt_required()
    @api.expect(place_model)  # Validates input against place_model
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Fetch the existing place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Restrict non-admin users to updating only their own places
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        place_data = api.payload
        
        # Non-admins cannot change the owner
        if not is_admin and 'owner_id' in place_data and place_data['owner_id'] != place.owner_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Admins can change the owner, but must verify the new owner exists
        if is_admin and 'owner_id' in place_data and not facade.get_user(place_data['owner_id']):
            return {'error': 'Owner not found'}, 400
        
        # Attempt to update the place via the facade
        try:
            updated_place = facade.update_place(place_id, place_data)
            return self._enrich_place_data(updated_place), 200  # Return enriched data
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any
    
# DELETE method to remove a place, requires JWT authentication and admin privileges
    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place (admin only)"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Restrict deletion to admin users only
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        # Fetch the existing place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Delete the place via the facade
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
        
    # Helper method to include additional data in place responses (duplicated for this class)
    def _enrich_place_data(self, place):
        """Helper method to include owner and amenities details in the response."""
        # Fetch the owner of the place
        owner = facade.get_user(place.owner_id)
        
        # Extract amenity IDs from the dynamic relationship and fetch each Amenity
        amenity_ids = [amenity.id for amenity in place.amenities.all()]  # Use .all() to get the list
        amenities = [facade.get_amenity(amenity_id) for amenity_id in amenity_ids]
        
        # Build the enriched place dictionary
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict() if owner else None
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities if amenity]
        return place_dict
