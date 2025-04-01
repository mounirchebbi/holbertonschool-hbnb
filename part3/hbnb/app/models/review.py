# app/models/review.py
from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        super().__init__()
        self.place = place  # Store place ID
        self.user = user  # Store user ID
        self.rating = int(rating)
        self.text = text

    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place,
            'user': self.user,
            'rating': self.rating,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
