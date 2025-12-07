from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable or use local MySQL as fallback
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set, check for Railway MySQL variables
if not DATABASE_URL:
    MYSQL_HOST = os.getenv("MYSQLHOST")
    MYSQL_PORT = os.getenv("MYSQLPORT", "3306")
    MYSQL_USER = os.getenv("MYSQLUSER") 
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQLDATABASE")
    
    if all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
        DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    else:
        # Fallback to local development
        DATABASE_URL = "mysql+pymysql://root:Ravish%4099055.@localhost:3306/pfa-b"

# For Railway MySQL deployment, ensure proper format
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

print(f"Using database: {DATABASE_URL.split('@')[0].split('://')[0]}://...@{DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
