from app.main import app
from app.database import create_tables
import os

# Create tables on startup (for serverless, this will run on each cold start)
if __name__ == "__main__":
    create_tables()

# Export the app for Vercel
app.debug = False 