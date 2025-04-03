# app/models/review.py
from .base_model import BaseModel
from app.database import db  # Import db from the new module

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating):
        super().__init__()
        self.text = text
        self.rating = int(rating)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
