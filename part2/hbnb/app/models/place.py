# app/models/place.py
import uuid
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner_id
        self.amenities = []
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    @classmethod
    def create(cls, title, description, price, latitude, longitude, owner):
        return cls(title, description, price, latitude, longitude, owner)
    
    def update(self, title, description, price, latitude, longitude):
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.updated_at = datetime.now()
    
    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.updated_at = datetime.now()
    
    def remove_amenity(self, amenity_id):
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
            self.updated_at = datetime.now()
    
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
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
