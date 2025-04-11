#!/bin/bash

# Base URL
BASE_URL="http://localhost:5000"

# Function to print response with a header
print_response() {
    echo "---------- $1 ----------"
    echo "$2" | jq .  # Pretty-print JSON
    echo ""
}

# Authentication (Login) - Get regular user token
user_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
    -H "Content-Type: application/json" \
    -d '{"email": "user@example.com", "password": "password123"}')
user_token=$(echo "$user_response" | jq -r '.access_token')
regular_user_id=$(echo "$user_response" | jq -r '.id')
print_response "Regular User Token" "$user_response"

# Authentication (Login) - Get admin token
admin_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@hbnb.io", "password": "admin1234"}')
admin_token=$(echo "$admin_response" | jq -r '.access_token')
print_response "Admin Token" "$admin_response"

# Users - Create a new user (Admin only)
user_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/users" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "securepass", "is_admin": false}')
user_id=$(echo "$user_create_response" | jq -r '.id')
print_response "New User Created" "$user_create_response"

# Users - Get user details (Public)
user_details=$(curl -s -X GET "${BASE_URL}/api/v1/users/${user_id}")
print_response "Public Get New User Details" "$user_details"

# Authentication (Login) - Get new user (John Doe) token
new_user_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
    -H "Content-Type: application/json" \
    -d '{"email": "john.doe@example.com", "password": "securepass"}')
new_user_token=$(echo "$new_user_response" | jq -r '.access_token')
print_response "New User Token (John Doe)" "$new_user_response"

# Users - Update user (Self, regular user)
user_update_response=$(curl -s -X PUT "${BASE_URL}/api/v1/users/${user_id}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${new_user_token}" \
    -d '{"first_name": "Johnny", "last_name": "Doe"}')
print_response "New User Self Update" "$user_update_response"

# Users - Update user as Admin (including email/password)
admin_update_response=$(curl -s -X PUT "${BASE_URL}/api/v1/users/${user_id}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"email": "update.john.doe@example.com", "password": "newsecurepass", "is_admin": true}')
print_response "Admin Updates New User" "$admin_update_response"

# Amenities - Create a new amenity (Admin only)
amenity_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/amenities" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${admin_token}" \
    -d '{"name": "Parking", "description": "Free parking space"}')
amenity_id=$(echo "$amenity_create_response" | jq -r '.id')
print_response "Created Amenity" "$amenity_create_response"

# Amenities - Get all amenities (Public)
all_amenities=$(curl -s -X GET "${BASE_URL}/api/v1/amenities")
print_response "Public Get All Amenities" "$all_amenities"

# Amenities - Get amenity by ID (Public)
amenity_details=$(curl -s -X GET "${BASE_URL}/api/v1/amenities/${amenity_id}")
print_response "Public Get Amenity by ID" "$amenity_details"

# Places - Get all places (Public)
all_places=$(curl -s -X GET "${BASE_URL}/api/v1/places")
print_response "Public Get All Places" "$all_places"

# Extract place IDs from initialized data
place1_id=$(echo "$all_places" | jq -r '.[0].id')  # Cozy Cottage
place2_id=$(echo "$all_places" | jq -r '.[1].id')  # City Apartment

# Places - Create a new place (Authenticated, new user)
place_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/places" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${new_user_token}" \
    -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place\", \"price\": 100.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"${user_id}\", \"amenities\": [\"${amenity_id}\"]}")
place_id=$(echo "$place_create_response" | jq -r '.id')
print_response "New User Creates New Place" "$place_create_response"

# Places - Get place by ID (Public)
place_details=$(curl -s -X GET "${BASE_URL}/api/v1/places/${place_id}")
print_response "Public Get New Place by ID" "$place_details"

# Reviews - Create a review (Authenticated, regular user)
review_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/reviews" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${user_token}" \
    -d "{\"user_id\": \"${regular_user_id}\", \"place_id\": \"${place_id}\", \"rating\": 5, \"text\": \"Fantastic stay!\"}")
review_id=$(echo "$review_create_response" | jq -r '.id')
print_response "Regular User Creates Review" "$review_create_response"
echo "Review ID: $review_id"  # Debug output

# Reviews - Get all reviews (Public)
all_reviews=$(curl -s -X GET "${BASE_URL}/api/v1/reviews")
print_response "Public Get All Reviews" "$all_reviews"

# Reviews - Get reviews by place (Public)
place_reviews=$(curl -s -X GET "${BASE_URL}/api/v1/places/${place_id}/reviews")
print_response "Public Get Reviews for Place (Cozy Apartment)" "$place_reviews"

# Reviews - Delete the new review (Admin only)
delete_review_response=$(curl -s -X DELETE "${BASE_URL}/api/v1/reviews/${review_id}" \
    -H "Authorization: Bearer ${admin_token}")
print_response "Admin Deletes New Review" "$delete_review_response"

# Delete the new place (Admin only)
delete_place_response=$(curl -s -X DELETE "${BASE_URL}/api/v1/places/${place_id}" \
    -H "Authorization: Bearer ${admin_token}")
print_response "Admin Deletes New Place" "$delete_place_response"

# Amenities - Delete the new amenity (Admin only)
delete_amenity_response=$(curl -s -X DELETE "${BASE_URL}/api/v1/amenities/${amenity_id}" \
    -H "Authorization: Bearer ${admin_token}")
print_response "Admin Deletes New Amenity" "$delete_amenity_response"

# Users - Delete the new user (Admin only)
delete_user_response=$(curl -s -X DELETE "${BASE_URL}/api/v1/users/${user_id}" \
    -H "Authorization: Bearer ${admin_token}")
print_response "Admin Deletes New User" "$delete_user_response"
