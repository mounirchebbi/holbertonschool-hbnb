# app/services/facade.py
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from werkzeug.security import generate_password_hash

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """Update an existing user's details."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        # Update only provided fields
        update_data = {}
        for key in ['first_name', 'last_name', 'email', 'is_admin']:
            if key in user_data:
                update_data[key] = user_data[key]
        if 'password' in user_data:
            update_data['password_hash'] = generate_password_hash(user_data['password'])

        self.user_repo.update(user_id, update_data)
        return self.get_user(user_id)
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
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
        
        # Update only provided fields
        update_data = {}
        for key in ['name', 'description']:
            if key in amenity_data:
                update_data[key] = amenity_data[key]

        self.amenity_repo.update(amenity_id, update_data)
        return self.get_amenity(amenity_id)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
