# run.py
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

# Populate the database with initial data
def initialize_database():
    # Create users
    admin_user = User('Admin', 'HBnB', 'admin@hbnb.io', 'admin1234', True)
    regular_user = User('Regular', 'User', 'user@example.com', 'password123', False)
    # Add users to session
    db.session.add_all([admin_user, regular_user])
    db.session.commit()  # Commit to generate IDs
    
    # Create amenities
    wifi = Amenity('Wi-Fi')
    pool = Amenity('Swimming Pool')
    # Add amenities to session
    db.session.add_all([wifi, pool])
    db.session.commit()  # Commit to generate IDs
    
    # Create places
    place1 = Place('Place1', 'place in the woods', 100.0, 40.7128, -74.0060, regular_user.id)
    place2 = Place('Place2', 'place in the city', 150.0, 34.0522, -118.2437, admin_user.id)
    # Add places to session
    db.session.add_all([place1, place2])
    db.session.commit()  # Commit to generate IDs
    
    # Add amenities to places after they are in the session
    place1.amenities = [wifi, pool]
    place2.amenities = [wifi]
    
    # Create reviews
    review1 = Review(place2.id, regular_user.id, 'very comfortable!', 4)
    review2 = Review(place1.id, admin_user.id, 'nice pool!', 5)
    # Add reviews to session
    db.session.add_all([review1, review2])
    
    # Final commit to persist all changes
    db.session.commit()
    print("Database initialized with sample data.")

# Create the Flask app instance
app = create_app()

# Ensure database operations occur within app context
with app.app_context():
    db.drop_all()  # Drop existing tables to clean start
    db.create_all()  # Create all tables
    initialize_database()

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
