# app/models/place.py
from base_model import BaseModel
from user import User
from amenity import Amenity
from review import Review

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        
        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner.id  # Store owner ID instead of instance
        self.amenities = []
        self.reviews = []  # Added to manage Place-Review relationship
    @classmethod
    def create(cls, title, description, price, latitude, longitude, owner):
        # validation
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        if price < 0:
            raise ValueError("Price must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")

        return cls(title, description, price, latitude, longitude, owner)
    
    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Must provide a valid Amenity instance")
        if amenity.id not in self.amenities:
            self.amenities.append(amenity.id)
            self.save()
    
    def remove_amenity(self, amenity_id):
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
            self.save()
    
    def get_amenities(self):
        return self.amenities  #  fetch Amenity objects

    def add_review(self, review):
        if not isinstance(review, Review):
            raise ValueError("Must provide a valid Review instance")
        if review.place != self.id:
            raise ValueError("Review must belong to this place")
        self.reviews.append(review.id)
        self.save()
    
    def get_reviews(self):
        return self.reviews  # fetch Review objects

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner,
            'amenities': self.amenities,
            'reviews': self.reviews,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
