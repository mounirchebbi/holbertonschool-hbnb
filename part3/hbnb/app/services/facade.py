# app/services/facade.py

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

        """
        # Pre-population logic is commented out until database initialization is set up
        # Pre-populate with an admin user
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="adminpass123",
            is_admin=True
        )
        self.user_repo.add(admin_user)
        # Pre-populate with a regular user
        regular_user = User(
            first_name="Regular",
            last_name="User",
            email="user@example.com",
            password="password123",
            is_admin=False
        )
        self.user_repo.add(regular_user)
        """

    """User Facade"""
    def create_user(self, user_data):
        # Extract data
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')
        password = user_data.get('password')
        is_admin = user_data.get('is_admin', False)

        # Validate inputs
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must not exceed 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must not exceed 50 characters")
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        if not password or len(password) < 6:
            raise ValueError("Password is required and must be at least 6 characters")
        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        # Create user
        user = User(first_name, last_name, email, password, is_admin)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        # Validate updated fields
        if 'first_name' in user_data:
            if not user_data['first_name'] or len(user_data['first_name']) > 50:
                raise ValueError("First name must not exceed 50 characters")
        if 'last_name' in user_data:
            if not user_data['last_name'] or len(user_data['last_name']) > 50:
                raise ValueError("Last name must not exceed 50 characters")
        if 'email' in user_data and user_data['email'] != user.email:
            if '@' not in user_data['email']:
                raise ValueError("Invalid email format")
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
        if 'password' in user_data:
            if len(user_data['password']) < 6:
                raise ValueError("Password must be at least 6 characters")
            user.hash_password(user_data['password'])

        # Update only provided fields
        update_data = {}
        for key in ['first_name', 'last_name', 'email', 'is_admin']:
            if key in user_data:
                update_data[key] = user_data[key]
        self.user_repo.update(user_id, update_data)
        return self.get_user(user_id)

    """Amenity Facade"""
    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        description = amenity_data.get('description', '')

        # Validate inputs
        if not name or len(name) > 50:
            raise ValueError("Name is required and must not exceed 50 characters")

        # Create amenity
        amenity = Amenity(name, description)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        # Validate updated fields
        if 'name' in amenity_data:
            if not amenity_data['name'] or len(amenity_data['name']) > 50:
                raise ValueError("Name must not exceed 50 characters")

        # Update only provided fields
        update_data = {}
        for key in ['name', 'description']:
            if key in amenity_data:
                update_data[key] = amenity_data[key]
        self.amenity_repo.update(amenity_id, update_data)
        return self.get_amenity(amenity_id)

    """Place Facade"""
    def create_place(self, place_data):
        title = place_data.get('title')
        description = place_data.get('description', '')
        price = place_data.get('price')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')
        owner_id = place_data.get('owner_id')
        amenity_ids = place_data.get('amenities', [])

        # Validate inputs
        if not title or len(title) > 100:
            raise ValueError("Title is required and must not exceed 100 characters")
        if not price or float(price) < 0:
            raise ValueError("Price is required and must be positive")
        if not latitude or not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude is required and must be between -90 and 90")
        if not longitude or not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude is required and must be between -180 and 180")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        for amenity_id in amenity_ids:
            if not self.get_amenity(amenity_id):
                raise ValueError(f"Amenity with ID {amenity_id} not found")

        # Create place
        place = Place(title, description, price, latitude, longitude, owner.id)
        place.amenities = amenity_ids  # Assign validated amenity IDs
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        # Validate updated fields
        if 'title' in place_data:
            if not place_data['title'] or len(place_data['title']) > 100:
                raise ValueError("Title must not exceed 100 characters")
        if 'price' in place_data:
            if float(place_data['price']) < 0:
                raise ValueError("Price must be positive")
        if 'latitude' in place_data:
            if not (-90 <= float(place_data['latitude']) <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data:
            if not (-180 <= float(place_data['longitude']) <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner.id
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                if not self.get_amenity(amenity_id):
                    raise ValueError(f"Amenity with ID {amenity_id} not found")

        # Update only provided fields
        update_data = {}
        for key in ['title', 'description', 'price', 'latitude', 'longitude', 'owner', 'amenities']:
            if key in place_data:
                update_data[key] = place_data[key]
        self.place_repo.update(place_id, update_data)
        return self.get_place(place_id)

    """Review Facade"""
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text')

        # Validate inputs
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        if not rating or not 1 <= int(rating) <= 5:
            raise ValueError("Rating is required and must be between 1 and 5")
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text is required")

        # Create review
        review = Review(place.id, user.id, rating, text)
        self.review_repo.add(review)
        place.add_review(review.id)  # Maintain relationship
        self.place_repo.update(place.id, {'reviews': place.reviews})  # Persist the updated reviews list
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return [self.get_review(review_id) for review_id in place.reviews if self.get_review(review_id)]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        # Validate updated fields
        if 'rating' in review_data:
            if not 1 <= int(review_data['rating']) <= 5:
                raise ValueError("Rating must be between 1 and 5")
        if 'text' in review_data:
            if not review_data['text'].strip():
                raise ValueError("Review text is required")

        # Update only provided fields
        update_data = {}
        for key in ['text', 'rating']:
            if key in review_data:
                update_data[key] = review_data[key]
        self.review_repo.update(review_id, update_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        place = self.get_place(review.place)
        if place and review_id in place.reviews:
            place.reviews.remove(review_id)  # Maintain relationship
            self.place_repo.update(place.id, {'reviews': place.reviews})  # Persist the updated reviews list
        self.review_repo.delete(review_id)
