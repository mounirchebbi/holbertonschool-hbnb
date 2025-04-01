#!/bin/bash

# Test Users
echo "Create User"
USER_ID=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "secure123"}' \
  | jq -r '.id')
echo "USER_ID: $USER_ID"

echo "Get User"
curl -s -X GET http://localhost:5000/api/v1/users/$USER_ID

echo "Update User"
curl -s -X PUT http://localhost:5000/api/v1/users/$USER_ID \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Johnny", "last_name": "Doe", "email": "invalid", "password": "newpass456"}'

# Test Amenities
echo "Create Amenity"
AMENITY_ID=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi", "description": "High-speed internet"}' \
  | jq -r '.id')
echo "AMENITY_ID: $AMENITY_ID"

echo "List Amenities"
curl -s -X GET http://localhost:5000/api/v1/amenities/

echo "Get Amenity"
curl -s -X GET http://localhost:5000/api/v1/amenities/$AMENITY_ID

echo "Update Amenity"
curl -s -X PUT http://localhost:5000/api/v1/amenities/$AMENITY_ID \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi", "description": "Updated high-speed internet"}'

# Test Places
echo "Create Place"
PLACE_ID=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Cozy Cabin\", \"price\": 100.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY_ID\"]}" \
  | jq -r '.id')
echo "PLACE_ID: $PLACE_ID"

echo "List Places"
curl -s -X GET http://localhost:5000/api/v1/places/

echo "Get Place"
curl -s -X GET http://localhost:5000/api/v1/places/$PLACE_ID

echo "Update Place"
curl -s -X PUT http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Updated Cabin\", \"price\": 120.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY_ID\"]}"


echo "Create Review (POST /api/v1/reviews/)"
REVIEW_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Great stay, very comfortable!\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "$REVIEW_RESPONSE"
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | jq -r '.id')
echo "REVIEW_ID: $REVIEW_ID"

echo "List All Reviews (GET /api/v1/reviews/)"
curl -s -X GET http://localhost:5000/api/v1/reviews/

echo "Get Specific Review (GET /api/v1/reviews/<review_id>)"
curl -s -X GET http://localhost:5000/api/v1/reviews/"$REVIEW_ID"

echo "Get Reviews for Place (GET /api/v1/places/<place_id>/reviews)"
curl -s -X GET http://localhost:5000/api/v1/places/"$PLACE_ID"/reviews

echo "Update Review (PUT /api/v1/reviews/<review_id>)"
curl -s -X PUT http://localhost:5000/api/v1/reviews/"$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated: Even better than expected!", "rating": 4}'

echo "Delete Review (DELETE /api/v1/reviews/<review_id>)"
curl -s -X DELETE http://localhost:5000/api/v1/reviews/"$REVIEW_ID"
