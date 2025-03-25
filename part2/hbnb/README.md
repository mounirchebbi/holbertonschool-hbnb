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

### Business Logic Layer
The business logic layer is implemented in the app/models/ directory and consists of 4 core entities: User, Place, Review, and Amenity. These classes inherit from a BaseModel to provide common functionality like unique IDs and timestamps.

## Entities and Responsibilities

# BaseModel
`description`: A base class providing common attributes and methods for all entities.
`Attributes`:
id (String): Unique identifier (UUID).
created_at (DateTime): Creation timestamp.
updated_at (DateTime): Last update timestamp.
`Methods`:
save(): Updates the updated_at timestamp.
update(data): Updates attributes from a dictionary and calls save().
`Responsibility`: Ensures all entities have consistent foundational behavior.

# User
`description`: Represents a user who can own places and write reviews.
`Attributes`:
first_name (String): Required, max 50 characters.
last_name (String): Required, max 50 characters.
email (String): Required, must be a valid email format.
password_hash (String): Hashed password for security.
is_admin (Boolean): Defaults to False.
`Methods`:
register(): Class method to create a new user + validation.
verify_password(password): Checks if a password matches the hash.
to_dict(): Serializes the user to a dictionary.
`Responsibility`: Manages user data, authentication, and serves as the owner of places or author of reviews.

# Place
`description`: Represents a location (e.g., a rental property) owned by a user.
`Attributes`:
title (String): Required, max 100 characters.
description (String): Optional description.
price (Float): Must be positive.
latitude (Float): Between -90 and 90.
longitude (Float): Between -180 and 180.
owner (String): ID of the owning User.
amenities (List): List of Amenity IDs (many-to-many).
reviews (List): List of Review IDs (one-to-many).
`Methods`:
create(): Class method to instantiate a place + validation.
add_amenity(amenity): Adds an amenity to the place.
remove_amenity(amenity_id): Removes an amenity.
add_review(review): Adds a review to the place.
get_amenities(): Returns the list of amenity IDs.
get_reviews(): Returns the list of review IDs.
to_dict(): Serializes the place to a dictionary.
`Responsibility`: Manages place details, its amenities, and associated reviews, ensuring data integrity through validation.

# Review
`description`: Represents a user’s review of a place.
`Attributes`:
place (String): ID of the reviewed Place.
user (String): ID of the authoring User.
rating (Integer): Between 1 and 5.
text (String): Required review content.
`Methods`:
create(): Class method to create a review and link it to the place + validation.
to_dict(): Serializes the review to a dictionary.
Responsibility: Captures feedback on a place, linking it to both a user and a place, with validation for rating and text.

# Amenity
`description`: Represents a feature available at a place (e.g., Wi-Fi, parking).
`Attributes`:
name (String): Required, max 50 characters.
description (String): Optional description.
`Methods`:
create(): Class method to instantiate an amenity + validation.
to_dict(): Serializes the amenity to a dictionary.
`Responsibility`: Defines reusable features that can be associated with multiple places.

# Relationships
`User-Place`: One-to-many (a user can own multiple places).
`Place-Review`: One-to-many (a place can have multiple reviews).
`Place-Amenity`: Many-to-many (a place can have multiple amenities, and an amenity can belong to multiple places).

## Class usage examples:

# User
`create:`
```
new_user = User.register(
    first_name="Alice",
    last_name="Smith",
    email="alice.smith@example.com",
    password="securepass123"
)
```

`update:`
```
new_user.update({
    "first_name": "Alicia",
    "last_name": "Smithson",
    "email": "alicia.smithson@example.com"
})
```

# Place
`create:`
```
new_place = Place.create(
    title="Cozy Cottage",
    description="A lovely retreat in the woods",
    price=120.50,
    latitude=45.678,
    longitude=-78.901,
    owner=new_user  # Pass the User instance created above
)
```

`update:`
```
new_place.update({
    "title": "Luxury Cozy Cottage",
    "description": "A luxurious retreat with modern amenities",
    "price": 150.75,
    "latitude": 45.679,
    "longitude": -78.902
})
```

# Review
`create:`
```

new_review = Review.create(
    place=new_place,  # Pass the Place instance
    user=new_user,    # Pass the User instance
    rating=4,
    text="Really enjoyed the stay, great location!"
)
```

# Amenity
`create:`
```
new_amenity = Amenity.create(
    name="Wi-Fi",
    description="High-speed internet access"
)
"Add the amenity to the place"
new_place.add_amenity(new_amenity)
```


## Installation and Running

- pip install -r requirements.txt
- python3 run.py
