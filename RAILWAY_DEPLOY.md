# Railway Deployment Configuration

## Step 1: Create a Railway Account
1. Go to https://railway.app
2. Sign up with GitHub or email
3. Create a new project

## Step 2: Add MySQL Database
1. In your Railway dashboard, click "New"
2. Select "Database" > "MySQL"
3. Railway will automatically create a MySQL instance
4. Note: Railway will provide DATABASE_URL environment variable automatically

## Step 3: Deploy Your Application
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Dockerfile
3. Set environment variables in Railway dashboard:
   - JWT_SECRET=your_secure_jwt_secret_here
   - JWT_ALGORITHM=HS256

## Step 4: Database Migration
After deployment, you may need to run database migrations:
1. Use Railway's CLI or web terminal
2. Run: `python -c "from schema.models import *; from db.database import engine; Base.metadata.create_all(bind=engine)"`

## Environment Variables Railway Provides Automatically:
- PORT (the port your app should listen on)
- DATABASE_URL (MySQL connection string)
- RAILWAY_ENVIRONMENT (production/development)

## Environment Variables You Need to Set:
- JWT_SECRET (your secure JWT secret key)
- JWT_ALGORITHM (HS256)

## Notes:
- The app uses MySQL with SQLAlchemy ORM both locally and on Railway
- CORS is configured to allow all origins for development
- Health check endpoint is available at `/`
- Database tables will be created automatically on startup
- PyMySQL is used as the MySQL driver for SQLAlchemy