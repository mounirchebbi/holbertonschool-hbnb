# app/models/base_model.py

from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # Ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        """Optional: Keep this method for compatibility with existing logic."""
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data):
        """Optional: Keep this method for compatibility with existing logic."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
