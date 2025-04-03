# app/models/amenity.py

from .base_model import BaseModel
from app.database import db  # Import db from the new module

# Amenity model for place features
class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    # Amenity attribute
    name = db.Column(db.String(50), nullable=False)
    
    # Relationships (backref 'places' defined in Place model)
    
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def to_dict(self):
        """Convert amenity object to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
