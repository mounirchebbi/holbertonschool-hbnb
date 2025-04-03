from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app

api = Namespace('places', description='Place operations')

# Define the models for related entities
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
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place_data = api.payload
        if not is_admin and place_data['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        if is_admin and not facade.get_user(place_data['owner_id']):
            return {'error': 'Owner not found'}, 400
        try:
            new_place = facade.create_place(place_data)
            return self._enrich_place_data(new_place), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [self._enrich_place_data(place) for place in places], 200

    def _enrich_place_data(self, place):
        """Helper method to include owner and amenities details in the response."""
        owner = facade.get_user(place.owner_id)
        # Extract amenity IDs from the dynamic relationship and fetch each Amenity
        amenity_ids = [amenity.id for amenity in place.amenities.all()]  # Use .all() to get the list of Amenity objects
        amenities = [facade.get_amenity(amenity_id) for amenity_id in amenity_ids]
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict() if owner else None
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities if amenity]
        return place_dict

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return self._enrich_place_data(place), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        place_data = api.payload
        if not is_admin and 'owner_id' in place_data and place_data['owner_id'] != place.owner_id:
            return {'error': 'Unauthorized action'}, 403
        if is_admin and 'owner_id' in place_data and not facade.get_user(place_data['owner_id']):
            return {'error': 'Owner not found'}, 400
        try:
            updated_place = facade.update_place(place_id, place_data)
            return self._enrich_place_data(updated_place), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    def _enrich_place_data(self, place):
        """Helper method to include owner and amenities details in the response."""
        owner = facade.get_user(place.owner_id)
        # Extract amenity IDs from the dynamic relationship and fetch each Amenity
        amenity_ids = [amenity.id for amenity in place.amenities.all()]  # Use .all() to get the list of Amenity objects
        amenities = [facade.get_amenity(amenity_id) for amenity_id in amenity_ids]
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict() if owner else None
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities if amenity]
        return place_dict
