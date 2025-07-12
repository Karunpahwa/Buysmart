# Supabase Setup Guide for BuySmart

## 1. Get Your Supabase Database URL

1. Go to your Supabase project dashboard: https://supabase.com/dashboard/project/oobtloagmckwkxhdicrz
2. Navigate to **Settings** → **Database**
3. Find the **Connection string** section
4. Copy the **URI** connection string (it should look like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.oobtloagmckwkxhdicrz.supabase.co:5432/postgres
   ```

## 2. Create Environment File

Create a `.env` file in the `backend` directory:

```bash
cd backend
cp env.example .env
```

## 3. Update Environment Variables

Edit the `.env` file and replace the `DATABASE_URL` with your Supabase connection string:

```env
# Database - Replace with your Supabase connection string
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.oobtloagmckwkxhdicrz.supabase.co:5432/postgres

# JWT Secret (generate a secure random string)
SECRET_KEY=your-super-secret-jwt-key-here

# Other settings...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
ENVIRONMENT=development
```

## 4. Generate Secure JWT Secret

Generate a secure JWT secret:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the output as your `SECRET_KEY` in the `.env` file.

## 5. Test Database Connection

Run the backend to test the connection:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## 6. Database Schema

The application will automatically create the required tables when it starts:

- `users` - User accounts and authentication
- `requirements` - Buyer requirements
- `listings` - OLX listings
- `messages` - Communication between buyers and sellers

## 7. Supabase Row Level Security (RLS)

For production, consider enabling RLS policies in Supabase:

1. Go to **Authentication** → **Policies**
2. Enable RLS on tables
3. Create policies for user-specific data access

## 8. Environment Variables for Deployment

For Vercel deployment, set these environment variables:

- `DATABASE_URL`: Your Supabase connection string
- `SECRET_KEY`: Your JWT secret
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30

## 9. Frontend Configuration

Update the frontend API base URL in `frontend/src/services/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

For production, set `VITE_API_BASE_URL` to your deployed backend URL.

## Troubleshooting

### Connection Issues
- Verify the connection string format
- Check if your IP is allowed in Supabase
- Ensure the password is correct

### SSL Issues
If you get SSL errors, add `?sslmode=require` to your connection string:
```
postgresql://postgres:[PASSWORD]@db.oobtloagmckwkxhdicrz.supabase.co:5432/postgres?sslmode=require
```

### Port Issues
If port 8000 is in use, use a different port:
```bash
uvicorn app.main:app --reload --port 8001
``` 