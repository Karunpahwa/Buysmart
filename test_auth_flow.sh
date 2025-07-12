#!/bin/bash

echo "🧪 Testing BuySmart Authentication Flow"
echo "======================================"

# Test 1: Health Check
echo "1. Testing health endpoint..."
curl -s -X GET http://localhost:8000/health | jq .

# Test 2: Register new user
echo -e "\n2. Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email": "testuser2@example.com", "password": "testpass123"}')
echo $REGISTER_RESPONSE | jq .

# Test 3: Login
echo -e "\n3. Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=testuser2@example.com&password=testpass123')
echo $LOGIN_RESPONSE | jq .

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

# Test 4: Get current user with valid token
echo -e "\n4. Testing /me endpoint with valid token..."
curl -s -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# Test 5: Test protected endpoint (requirements)
echo -e "\n5. Testing protected endpoint (create requirement)..."
curl -s -X POST http://localhost:8000/api/requirements/ \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_query": "MacBook Pro", "category": "electronics", "budget_min": 80000, "budget_max": 120000, "timeline": "flexible", "deal_breakers": [], "condition_preferences": []}' | jq .

# Test 6: Test invalid token
echo -e "\n6. Testing invalid token..."
curl -s -X GET http://localhost:8000/api/auth/me \
  -H 'Authorization: Bearer invalid_token' | jq .

# Test 7: Test frontend proxy
echo -e "\n7. Testing frontend proxy..."
curl -s -X GET http://localhost:5173/api/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq .

echo -e "\n✅ Authentication flow test completed!" 