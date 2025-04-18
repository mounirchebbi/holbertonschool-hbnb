
# HBNB Front-End

This repository contains the front-end files for the **HBNB Web Application**, responsible for user interaction, listing places, user authentication, and reviews.

## Structure

```
hbnb/
├── images/
├── index.html
├── login.html
├── place.html
├── add_review.html
├── styles.css
├── scripts.js
```

## Pages Overview

### `index.html`
- Landing page that displays a list of available places.
- Includes a price filter dropdown.
- Login/logout UI based on authentication state.

### `login.html`
- User login form.
- Submits credentials to back-end API.
- On success, stores JWT token in cookies.

### `place.html`
- Displays informations for a selected place.
- Shows existing reviews.
- Only Authenticated users can submit new reviews.

### `add_review.html`
- Dedicated page to add a review.
- Requires authentication.
- Automatically fills the place ID from URL query.

## Styling

All styles are defined in `styles.css`:
- Responsive and clean design using grid layouts.
- Styled buttons, cards, and form components.

## JavaScript Logic

Main logic located in `scripts.js`:
- Handles login/logout functionality.
- Fetches places, details, and reviews from the API.
- Renders UI elements dynamically.
- Manages JWT-based session with cookie storage.
- Submits new reviews with validation.

## Authentication

- JWT token is stored in cookies.
- UI changes based on login state.
- Only Logged-in users can post reviews., while guests can only view content.

## API Integration

All data is fetched from the following endpoints:
- `POST /api/v1/login` – Authenticates user.
- `GET /api/v1/places` – Gets list of all places.
- `GET /api/v1/places/:id` – Gets specific place details.
- `GET /api/v1/places/:id/reviews` – Lists reviews for a place.
- `POST /api/v1/reviews` – Creates a new review (auth required).

## Installation

To set up and run the HBnB application locally:

    - Clone the Repository (assumed step):
        If the project is in a Git repository, use:
```
    git clone <repository-url>
    cd hbnb
```


    - Install Dependencies:

      The requirements.txt file lists dependencies (Flask, Flask-RESTX, SQLAlchemy, flask_cors). Install them with:
```
    pip install -r requirements.txt
```
### Run the Application:

    1- Run the back-end in /part3/hbnb:

    - Configure your Mysql Database in /part3/hbnb/config.py  (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

    - The entry point is run.py, which initializes the database and starts the Flask server:
```
    python3 run.py
```

    2- Run the front-end in /part4:
```
     python3 -m http.server 8000
```
