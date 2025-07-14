#!/bin/bash
set -ex

# BuySmart API Test Script
# Tests: create requirement, list requirements

BASE_URL="http://127.0.0.1:8000"

echo "🧪 BuySmart API Test Script"
echo "=========================="

# Test 1: Health Check
echo "✅ Testing health endpoint..."
curl -s "$BASE_URL/health" | jq .
echo ""

# Test 2: Create Requirement
echo "✅ Testing create requirement..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/requirements/" \
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

# Test 3: List Requirements
echo "✅ Testing list requirements..."
curl -s -X GET "$BASE_URL/api/requirements/" | jq .
echo ""

echo "🎉 All tests completed!"
echo "==========================" 