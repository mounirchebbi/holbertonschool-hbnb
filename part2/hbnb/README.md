# HBnB - Property Rental

HBnB is a web app designed for managing property rentals, allowing users to register, create and manage rental places, add reviews, and handle amenities.

## Project Setup Overview

### Directory Structure and Purpose

    hbnb/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── amenities.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── facade.py
    │   ├── persistence/
    │       ├── __init__.py
    │       ├── repository.py
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── README.md



### File Descriptions

- `run.py`: Entry point to start the Flask application
- `config.py`: Contains configuration classes for different environments
- `requirements.txt`: Lists all Python package dependencies
- `app/__init__.py`: Creates and configures the Flask application and API
- `app/api/v1/*.py`: Define RESTful API endpoints for different resources
- `app/models/*.py`: Contain class definitions for core entities
- `app/services/facade.py`: Implements business logic and coordinates between models and persistence
- `app/persistence/repository.py`: Provides data storage abstraction (currently in-memory)

## Installation and Running

- pip install -r requirements.txt
- python3 run.py
