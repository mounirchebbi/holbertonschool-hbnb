# app/models/amenity.py
import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name, description):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    @classmethod
    def create(cls, name, description):
        return cls(name, description)
    
    def update(self, name, description):
        self.name = name
        self.description = description
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
