#!/bin/bash

# File: test_api_endpoints.sh

# Base URL
BASE_URL="http://localhost:5000"

# Authentication (Login) - Get user token (regular user)
user_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}')
user_token=$(echo "$user_response" | jq -r '.access_token')
echo "---------- Regular User Token ----------: $user_token"

# Authentication (Login) - Get admin token (admin user)
admin_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "adminpass123"}')
admin_token=$(echo "$admin_response" | jq -r '.access_token')
echo "---------- Admin Token ----------: $admin_token"

# Users - Create a new user (Admin only)
user_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/users/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${admin_token}" \
     -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "securepass", "is_admin": false}')
user_id=$(echo "$user_create_response" | jq -r '.id')
echo "---------- New User ID ----------: $user_id"

# Users - Get user details (Public)
echo "---------- public get New User details ----------"
curl -s -X GET "${BASE_URL}/api/v1/users/${user_id}"

# Authentication (Login) - Get new_user john doe token
user_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "john.doe@example.com", "password": "securepass"}')
user_token=$(echo "$user_response" | jq -r '.access_token')
echo "---------- NEW User Token ----------: $user_token"


# Users - Update user (Self, regular user) (user id != current user id)
echo "---------- New User self update ----------"
curl -s -X PUT "${BASE_URL}/api/v1/users/${user_id}" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${user_token}" \
     -d '{"first_name": "Johnny", "last_name": "Doe"}'

# Users - Update user as Admin (including email/password)
echo "---------- Admin updates New User ----------"

curl -s -X PUT "${BASE_URL}/api/v1/users/${user_id}" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${admin_token}" \
     -d '{"email": "update.john.doe@example.com", "password": "newsecurepass", "is_admin": true}'

# Amenities - Create a new amenity (Admin only)
amenity_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/amenities/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${admin_token}" \
     -d '{"name": "WiFi", "description": "High-speed internet"}')
amenity_id=$(echo "$amenity_create_response" | jq -r '.id')
echo "---------- Created Amenity ID ----------: $amenity_id"

# Amenities - Get all amenities (Public)
echo "---------- public get all amenities ----------"

curl -s -X GET "${BASE_URL}/api/v1/amenities/"

# Amenities - Get amenity by id (Public)
echo "---------- public get amenity by id ----------"

curl -s -X GET "${BASE_URL}/api/v1/amenities/${amenity_id}"

# Places - Create a new place (Authenticated, regular user)
echo "---------- new user (non admin) creates new place ----------"

place_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/places/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${user_token}" \
     -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place\", \"price\": 100.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"${user_id}\", \"amenities\": [\"${amenity_id}\"]}")
place_id=$(echo "$place_create_response" | jq -r '.id')
echo "Created Place ID: $place_id"
