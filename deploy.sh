#!/bin/bash

# BuySmart Assistant - Vercel Deployment Script

echo "🚀 Starting BuySmart Assistant deployment to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << EOF
# Database URL (PostgreSQL)
DATABASE_URL=your_postgresql_database_url_here

# JWT Secret (generate a random string)
JWT_SECRET=your_jwt_secret_here

# Frontend API URL
VITE_API_BASE_URL=/api
EOF
    echo "📝 Please update .env file with your actual values before deploying."
    echo "   - Get a PostgreSQL database from Supabase, Railway, or Neon"
    echo "   - Generate a JWT secret (you can use: openssl rand -hex 32)"
    exit 1
fi

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at the URL shown above."
echo ""
echo "📋 Next steps:"
echo "1. Test your API at: https://your-domain.vercel.app/api/docs"
echo "2. Test your frontend at: https://your-domain.vercel.app"
echo "3. Set up environment variables in Vercel dashboard if needed"
echo "4. Configure custom domain if desired" 