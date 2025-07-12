#!/usr/bin/env python3
"""
Setup script for BuySmart Supabase configuration
"""

import os
import secrets

def create_env_file():
    """Create .env file with Supabase configuration"""
    
    # Get Supabase password from user
    print("🔧 BuySmart Supabase Setup")
    print("=" * 40)
    
    supabase_password = input("Enter your Supabase database password: ").strip()
    
    if not supabase_password:
        print("❌ Password is required!")
        return
    
    # Generate JWT secret
    jwt_secret = secrets.token_urlsafe(32)
    
    # Create .env content
    env_content = f"""# Database - Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:{supabase_password}@db.oobtloagmckwkxhdicrz.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY={jwt_secret}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# OLX Scraping
OLX_BASE_URL=https://www.olx.in
SCRAPER_DELAY=2
MAX_CONCURRENT_SCRAPES=5

# App Settings
DEBUG=true
ENVIRONMENT=development
"""
    
    # Write to .env file
    env_path = "backend/.env"
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"✅ Created {env_path}")
    print(f"🔑 JWT Secret: {jwt_secret}")
    print("\n📋 Next steps:")
    print("1. Test the connection: cd backend && python -m uvicorn app.main:app --reload")
    print("2. Check the API docs at: http://localhost:8000/docs")
    print("3. Start the frontend: cd frontend && npm run dev")

if __name__ == "__main__":
    create_env_file() 