# app/models/place.py
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner  # Store owner ID
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.save()

    def remove_amenity(self, amenity_id):
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
            self.save()

    def get_amenities(self):
        return self.amenities

    def add_review(self, review_id):
        if review_id not in self.reviews:
            self.reviews.append(review_id)
            self.save()

    def get_reviews(self):
        return self.reviews

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
