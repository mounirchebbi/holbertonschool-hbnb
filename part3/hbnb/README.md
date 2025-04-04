# HBnB - Property Rental - part 3

HBnB is a web app designed for managing property rentals, allowing users to register, create and manage rental places, add reviews, and handle amenities.

## Project Setup Overview

### Directory Structure and Purpose
```
hbnb/
├── app/
│   ├── __init__.py                  # Application factory and initialization of Flask app and extensions
│   ├── api/
│   │   ├── __init__.py              # API module initialization (empty)
│   │   ├── v1/
│   │   │   ├── __init__.py          # API v1 namespace initialization (empty)
│   │   │   ├── auth.py             # Defines authentication endpoints (e.g., login with JWT)
│   │   │   ├── users.py            # Defines REST API endpoints for user operations
│   │   │   ├── places.py           # Defines REST API endpoints for place operations
│   │   │   ├── reviews.py          # Defines REST API endpoints for review operations
│   │   │   ├── amenities.py        # Defines REST API endpoints for amenity operations
│   ├── models/
│   │   ├── __init__.py              # Models module initialization (empty)
│   │   ├── base_model.py           # Defines the abstract base class for all models with common attributes
│   │   ├── user.py                 # Defines the User model with attributes and methods (e.g., password hashing)
│   │   ├── place.py                # Defines the Place model with attributes and relationships
│   │   ├── review.py               # Defines the Review model with attributes and relationships
│   │   ├── amenity.py              # Defines the Amenity model with attributes
│   │   ├── place_amenity.py        # Defines the association table for the many-to-many Place-Amenity relationship
│   ├── services/
│   │   ├── __init__.py              # Services module initialization and facade instance creation
│   │   ├── facade.py               # Provides a facade layer for business logic and interaction with repositories
│   ├── persistence/
│   │   ├── __init__.py              # Persistence module initialization (empty)
│   │   ├── repository.py           # Defines abstract Repository class and SQLAlchemy/InMemory implementations
│   │   ├── user_repository.py      # Implements User-specific repository methods using SQLAlchemy
│   │   ├── place_repository.py     # Implements Place-specific repository methods using SQLAlchemy
│   │   ├── review_repository.py    # Implements Review-specific repository methods using SQLAlchemy
│   │   ├── amenity_repository.py   # Implements Amenity-specific repository methods using SQLAlchemy
│   ├── database.py                  # Initializes the SQLAlchemy database instance (db)
├── run.py                           # Entry point for running the Flask app and initializing the database
├── config.py                        # Contains configuration classes for the Flask application
├── requirements.txt                 # Lists Python dependencies required for the project
├── README.md                        # Provides documentation and information about the project
```
## APP Layers

### 1. API Layer

    - Role: Handles client requests and responses for the HBnB app via REST endpoints.
    - Where: app/api/v1/ (e.g., users.py, places.py, reviews.py, auth.py).
    - What It Does: Defines routes like /api/v1/places, validates inputs (e.g., place title), checks JWT authentication, and formats JSON responses (e.g., place.to_dict()).
    - Example: POST /api/v1/users in users.py creates a user by calling the facade.

### 2. Business Logic Layer

    - Role: Manages HBnB’s core rules and processes.
    - Where: app/services/facade.py (HBnBFacade).
    - What It Does: Enforces rules (e.g., users can’t review their own place), validates data (e.g., rating 1-5), and coordinates with repositories.
    `Example: create_place() in facade.py ensures valid coordinates and owner, then saves the place.`

### 3. Persistence Layer

    - Role: Stores and retrieves HBnB data in the database.
    - Where: app/persistence/ (e.g., user_repository.py, place_repository.py) and app/models/.
    - What It Does: Maps models (e.g., User, Place) to tables via SQLAlchemy and handles CRUD operations (e.g., add, get).
    `Example: PlaceRepository.add() saves a new place to the places table.`
    
#### Entities
```
- User (app/models/user.py)
Attributes: id, first_name, last_name, email, password, is_admin, created_at, updated_at.
Table: users.

- Place (app/models/place.py)
Attributes: id, title, description, price, latitude, longitude, owner_id, created_at, updated_at.
Table: places.

- Amenity (app/models/amenity.py)
Attributes: id, name, created_at, updated_at.
Table: amenities.

- Review (app/models/review.py)
Attributes: id, text, rating, place_id, user_id, created_at, updated_at.
Table: reviews.

- Place_Amenity (app/models/place_amenity.py)
Attributes: place_id, amenity_id.
Table: place_amenity.
```


#### Relatioships
```
User ↔ Place: One-to-Many (User.places, Place.owner_id, backref='owner').
User ↔ Review: One-to-Many (User.reviews, Review.user_id, backref='author').
Place ↔ Review: One-to-Many (Place.reviews, Review.place_id, backref='place').
Place ↔ Amenity: Many-to-Many (via place_amenity table, Place.amenities, Amenity.places).
All use lazy='dynamic' for flexible querying, with BaseModel providing common fields.
```

### How They Work Together

    - Flow:
        API gets a request (e.g., POST /api/v1/places), validates it, and calls the facade.
        Facade checks rules (e.g., valid price) and tells the repository to save the place.
        Repository uses SQLAlchemy to store it in the database.
        Data flows back: repository → facade → API, which sends a JSON response.
    `Example: Creating a place starts at places.py, goes to facade.create_place(), then place_repo.add(), and returns the new place’s details.`


### Installation

- To set up and run the HBnB application locally:

    Clone the Repository (assumed step):
        If the project is in a Git repository, use:
```
    git clone <repository-url>
    cd hbnb
```


Install Dependencies:

    - The requirements.txt file lists dependencies (e.g., Flask, Flask-RESTX, SQLAlchemy). Install them with:
```
    pip install -r requirements.txt
```
Run the Application:

    - The entry point is run.py, which initializes the database and starts the Flask server:
```
    python run.py
```
Running Tests from test_api_endpoints.sh

Make the script executable and run it:
```
    chmod +x test_api_endpoints.sh
    ./test_api_endpoints.sh
```
