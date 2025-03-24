# app/models/review.py
from base_model import BaseModel
from user import User
from place import Place

class Review(BaseModel):
    def __init__(self, place, user, rating, text):
        super().__init__()
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        
        self.place = place.id
        self.user = user.id
        self.rating = int(rating)
        self.text = text

    @classmethod
    def create(cls, place, user, rating, text):
        review = cls(place, user, rating, text)
        place.add_review(review)  # Maintain relationship
        return review
    
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
