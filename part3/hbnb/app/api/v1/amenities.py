# app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for creation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, default='', description='Description of the amenity')
})

# Model for updates (all fields optional)
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        current_user = get_jwt_identity()
        # Only admins can create amenities
        if not current_user['is_admin']:
            return {'error': 'Unauthorized action'}, 403

        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of amenities retrieved')
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):

        current_user = get_jwt_identity()
        # Only admins can update amenities
        if not current_user['is_admin']:
            return {'error': 'Unauthorized action'}, 403
        
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
