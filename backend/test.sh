#!/bin/bash

# BuySmart API Test Script
# Tests: register, login, create requirement, list requirements

BASE_URL="http://127.0.0.1:8000"
TEST_EMAIL="testuser@example.com"
TEST_PASSWORD="testpass123"

echo "🧪 BuySmart API Test Script"
echo "=========================="

# Test 1: Health Check
echo "✅ Testing health endpoint..."
curl -s "$BASE_URL/health" | jq .
echo ""

# Test 2: Register User
echo "✅ Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\", \"password\":\"$TEST_PASSWORD\"}")

echo "Register response:"
echo "$REGISTER_RESPONSE" | jq .
echo ""

# Test 3: Login and Get Token
echo "✅ Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_EMAIL&password=$TEST_PASSWORD")

echo "Login response:"
echo "$LOGIN_RESPONSE" | jq .

# Extract token
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')
echo "Token: $TOKEN"
echo ""

# Test 4: Get Current User
echo "✅ Testing get current user..."
curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# Test 5: Create Requirement
echo "✅ Testing create requirement..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/requirements/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_query": "macbook pro 2020",
    "category": "electronics",
    "budget_min": 30000,
    "budget_max": 90000,
    "timeline": "flexible",
    "deal_breakers": ["broken keyboard", "water damage"],
    "condition_preferences": ["like new", "good"]
  }')

echo "Create requirement response:"
echo "$CREATE_RESPONSE" | jq .
echo ""

# Test 6: List Requirements
echo "✅ Testing list requirements..."
curl -s -X GET "$BASE_URL/api/requirements/" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# Test 7: Test without auth (should fail)
echo "✅ Testing unauthorized access (should fail)..."
curl -s -X GET "$BASE_URL/api/requirements/" | jq .
echo ""

echo "🎉 All tests completed!"
echo "==========================" 