# app/models/review.py

from .base_model import BaseModel
from app.database import db  # Import db from the new module

# Review model for user feedback on places
class Review(BaseModel):
    __tablename__ = 'reviews'
    
    # Review attributes
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Relationships
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, place_id, user_id, text, rating):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.text = text
        self.rating = int(rating)
    
    def to_dict(self):
        """Convert review object to dictionary for API responses."""
        return {
            'id': self.id,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
