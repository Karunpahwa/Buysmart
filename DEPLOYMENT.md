# BuySmart Assistant - Vercel Deployment Guide

This guide will help you deploy the BuySmart Assistant to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Database**: You'll need a PostgreSQL database (recommended: Supabase, Railway, or Neon)

## Step 1: Prepare Your Database

### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database URL from Settings > Database
4. The URL format: `postgresql://username:password@host:port/database`

### Option B: Railway
1. Go to [railway.app](https://railway.app)
2. Create a new PostgreSQL database
3. Get your database URL from the database settings

### Option C: Neon
1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Get your database URL from the connection details

## Step 2: Set Up Environment Variables

Create a `.env` file in your project root:

```env
# Database
DATABASE_URL=your_postgresql_database_url_here

# JWT Secret (generate a random string)
JWT_SECRET=your_jwt_secret_here

# Frontend API URL (for development)
VITE_API_BASE_URL=/api
```

## Step 3: Deploy to Vercel

### Method A: Vercel CLI (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   ```bash
   vercel env add DATABASE_URL
   vercel env add JWT_SECRET
   ```

5. **Redeploy with environment variables**:
   ```bash
   vercel --prod
   ```

### Method B: GitHub Integration

1. **Push your code to GitHub**

2. **Connect to Vercel**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

3. **Configure Build Settings**:
   - Framework Preset: `Other`
   - Root Directory: `./` (root of your project)
   - Build Command: Leave empty (Vercel will use vercel.json)
   - Output Directory: `frontend/dist`

4. **Set Environment Variables**:
   - Go to Project Settings > Environment Variables
   - Add:
     - `DATABASE_URL`: Your PostgreSQL URL
     - `JWT_SECRET`: Your JWT secret
     - `VITE_API_BASE_URL`: `/api`

5. **Deploy**:
   - Click "Deploy"

## Step 4: Verify Deployment

1. **Check API Endpoints**:
   - Visit `https://your-domain.vercel.app/api/docs`
   - You should see the FastAPI documentation

2. **Test Frontend**:
   - Visit `https://your-domain.vercel.app`
   - The React app should load

3. **Test Authentication**:
   - Try registering a new user
   - Try logging in

## Step 5: Custom Domain (Optional)

1. **Add Custom Domain**:
   - Go to Project Settings > Domains
   - Add your custom domain
   - Follow the DNS configuration instructions

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure `package.json` has correct build scripts

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` is correct
   - Check that your database allows external connections
   - Ensure database is running

3. **API 404 Errors**:
   - Check that `vercel.json` routes are correct
   - Verify API endpoints are working locally

4. **Frontend Not Loading**:
   - Check browser console for errors
   - Verify API base URL is correct
   - Check that build completed successfully

### Debug Commands

```bash
# Check Vercel deployment status
vercel ls

# View deployment logs
vercel logs

# Redeploy
vercel --prod

# Check environment variables
vercel env ls
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret for JWT token signing | Yes |
| `VITE_API_BASE_URL` | Frontend API base URL | No (defaults to `/api`) |

## Database Migration

If you need to run database migrations:

1. **Local Development**:
   ```bash
   cd backend
   python -c "from app.database import create_tables; create_tables()"
   ```

2. **Production**:
   - The tables will be created automatically on first API call
   - Or you can trigger a deployment with environment variables set

## Monitoring

1. **Vercel Analytics**: Enable in project settings
2. **Error Tracking**: Consider adding Sentry
3. **Database Monitoring**: Use your database provider's monitoring tools

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **CORS**: Configure CORS settings in your FastAPI app
3. **Rate Limiting**: Consider adding rate limiting for production
4. **HTTPS**: Vercel provides HTTPS by default

## Performance Optimization

1. **Database Indexing**: Add indexes to frequently queried columns
2. **Caching**: Consider adding Redis for caching
3. **CDN**: Vercel provides global CDN automatically
4. **Image Optimization**: Use Vercel's image optimization

## Support

If you encounter issues:

1. Check the [Vercel Documentation](https://vercel.com/docs)
2. Review the [FastAPI Documentation](https://fastapi.tiangolo.com/)
3. Check the [React Documentation](https://reactjs.org/docs/)

## Next Steps

After successful deployment:

1. **Set up monitoring and logging**
2. **Configure CI/CD pipelines**
3. **Add automated testing**
4. **Set up backup strategies**
5. **Plan for scaling**

Your BuySmart Assistant should now be live and accessible at your Vercel domain! 🚀 