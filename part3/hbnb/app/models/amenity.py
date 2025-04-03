# app/models/amenity.py
from .base_model import BaseModel
from app.database import db  # Import db from the new module

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    # Relationships
    # 'places' backref is defined in Place model

    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description  # Kept for compatibility, though not persisted yet

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            #'description': self.description,  # Included for compatibility
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
