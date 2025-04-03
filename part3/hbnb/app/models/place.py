# app/models/place.py
from .base_model import BaseModel
from app.database import db  # Import db from the new module


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, description, price, latitude, longitude):
        super().__init__()
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
