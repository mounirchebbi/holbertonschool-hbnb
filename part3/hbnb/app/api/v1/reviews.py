# app/api/v1/reviews.py

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app

# API namespace for review operations
api = Namespace('reviews', description='Review operations')

# review model for input validation and API documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# review model for updates all fields are optional
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

# reviews operations
@api.route('/reviews')  # Base route for review collection
class ReviewList(Resource):
    # POST method to create a new review, requires JWT authentication
    @jwt_required()  # Ensures the request includes a valid JWT token
    @api.expect(review_model, validate=True)  # Validates input against review_model
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        review_data = api.payload
        
        # Verify the place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Prevent users from reviewing their own place
        if place.owner_id == current_user['id']:
            return {'error': 'You cannot review your own place'}, 400
        
        # Check if the user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user_id == current_user['id']:
                return {'error': 'You have already reviewed this place'}, 400
        
        # Override user_id with the authenticated user's ID for security
        review_data['user_id'] = current_user['id']
        
        # create the review via the facade
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors
    
    # GET method to retrieve all reviews, no authentication required
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Fetch all reviews from facade
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

# operations on review by ID
@api.route('/reviews/<review_id>')
class ReviewResource(Resource):
    # GET method to retrieve review details, no authentication required
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Fetch the review from the facade
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    # PUT method to update a review, requires JWT authentication
    @jwt_required()
    @api.expect(review_update_model, validate=True)  # Validates input against review_update_model
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Fetch the existing review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Restrict non-admin users to updating only their own reviews
        if not is_admin and review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        review_data = api.payload
        
        # Attempt to update the review via the facade
        try:
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400  # Return validation errors if any
    
    # DELETE a review, requires JWT authentication
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Fetch the existing review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        #  non-admin users delete only their own reviews
        if not is_admin and review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        # Delete review via facade
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

# reviews by place id
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    # GET method to retrieve all reviews for a place, no authentication required
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Verify the place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Fetch reviews for the place via the facade
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404
