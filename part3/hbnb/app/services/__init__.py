# app/services/__init__.py

from app.services.facade import HBnBFacade

# Singleton instance of the facade for service layer access
facade = HBnBFacade()
