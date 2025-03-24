# app/models/review.py
import uuid
from datetime import datetime

class Review:
    def __init__(self, place_id, user_id, rating, comment):
        self.id = str(uuid.uuid4())
        self.place = place_id
        self.user = user_id
        self.rating = int(rating)
        self.comment = comment
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    @classmethod
    def create(cls, place, user, rating, comment):
        return cls(place, user, rating, comment)
    
    def update(self, rating, comment):
        self.rating = int(rating)
        self.comment = comment
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'place': self.place,
            'user': self.user,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

