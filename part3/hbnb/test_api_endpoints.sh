#!/bin/bash

# File: test_api_endpoints.sh

# Base URL
BASE_URL="http://localhost:5000"

# Authentication (Login) - Get admin token (admin user)
admin_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "adminpass123"}')
admin_token=$(echo "$admin_response" | jq -r '.access_token')
if [ "$admin_token" == "null" ] || [ -z "$admin_token" ]; then
    echo "Error: Failed to get admin token. Response: $admin_response"
    exit 1
else
    echo "Admin Token: $admin_token"
fi

# Users - Create a new user (Admin only)
user_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/users/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${admin_token}" \
     -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "securepass", "is_admin": false}')
user_id=$(echo "$user_create_response" | jq -r '.id')
if [ "$user_id" == "null" ] || [ -z "$user_id" ]; then
    echo "Error: Failed to create user. Response: $user_create_response"
    exit 1
else
    echo "Created User ID: $user_id"
fi

# Authentication (Login) - Get user token (using newly created user)
user_response=$(curl -s -X POST "${BASE_URL}/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "john.doe@example.com", "password": "securepass"}')
user_token=$(echo "$user_response" | jq -r '.access_token')
if [ "$user_token" == "null" ] || [ -z "$user_token" ]; then
    echo "Error: Failed to get user token. Response: $user_response"
    exit 1
else
    echo "User Token: $user_token"
fi

# Users - Get user details (Public)
curl -s -X GET "${BASE_URL}/api/v1/users/${user_id}"

# Users - Update user (Self, regular user)
curl -s -X PUT "${BASE_URL}/api/v1/users/${user_id}" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${user_token}" \
     -d '{"first_name": "Johnny", "last_name": "Doe"}'

# Users - Update user as Admin (including email/password)
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
if [ "$amenity_id" == "null" ] || [ -z "$amenity_id" ]; then
    echo "Error: Failed to create amenity. Response: $amenity_create_response"
    exit 1
else
    echo "Created Amenity ID: $amenity_id"
fi

# Amenities - Get all amenities (Public)
curl -s -X GET "${BASE_URL}/api/v1/amenities/"

# Amenities - Get amenity by id (Public)
curl -s -X GET "${BASE_URL}/api/v1/amenities/${amenity_id}"

# Places - Create a new place (Authenticated, regular user)
place_create_response=$(curl -s -X POST "${BASE_URL}/api/v1/places/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${user_token}" \
     -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place\", \"price\": 100.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"${user_id}\", \"amenities\": [\"${amenity_id}\"]}")
place_id=$(echo "$place_create_response" | jq -r '.id')
if [ "$place_id" == "null" ] || [ -z "$place_id" ]; then
    echo "Error: Failed to create place. Response: $place_create_response"
    exit 1
else
    echo "Created Place ID: $place_id"
fi
