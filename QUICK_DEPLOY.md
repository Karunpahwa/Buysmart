# 🚀 Quick Deploy to Vercel

Get your BuySmart Assistant live in 5 minutes!

## Prerequisites

1. **Database**: Get a free PostgreSQL database from [Supabase](https://supabase.com)
2. **GitHub**: Push your code to GitHub
3. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)

## Step 1: Get a Database

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the connection string (starts with `postgresql://`)

## Step 2: Set Up Environment Variables

Create a `.env` file in your project root:

```bash
# Generate a JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Create .env file
cat > .env << EOF
DATABASE_URL=your_supabase_postgresql_url_here
JWT_SECRET=$JWT_SECRET
VITE_API_BASE_URL=/api
EOF
```

## Step 3: Deploy

### Option A: Use the deployment script
```bash
./deploy.sh
```

### Option B: Manual deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Step 4: Set Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add:
   - `DATABASE_URL`: Your Supabase PostgreSQL URL
   - `JWT_SECRET`: Your JWT secret
   - `VITE_API_BASE_URL`: `/api`

## Step 5: Test Your Deployment

1. **API**: Visit `https://your-domain.vercel.app/api/docs`
2. **Frontend**: Visit `https://your-domain.vercel.app`
3. **Register**: Create a new account
4. **Login**: Test authentication

## Troubleshooting

### Build Fails
- Check that all files are committed to GitHub
- Verify `requirements.txt` and `package.json` are correct

### Database Connection Error
- Verify your `DATABASE_URL` is correct
- Check that your database allows external connections

### Frontend Not Loading
- Check browser console for errors
- Verify API base URL is `/api`

## Support

- 📖 [Full Deployment Guide](DEPLOYMENT.md)
- 🐛 [Vercel Documentation](https://vercel.com/docs)
- 💬 [FastAPI Documentation](https://fastapi.tiangolo.com/)

Your BuySmart Assistant should now be live! 🎉 