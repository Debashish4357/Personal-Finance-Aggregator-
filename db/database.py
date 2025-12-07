from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for Railway MySQL environment variables first
MYSQL_HOST = os.getenv("MYSQLHOST")
MYSQL_PORT = os.getenv("MYSQLPORT", "3306")
MYSQL_USER = os.getenv("MYSQLUSER") 
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQLDATABASE")

# Build DATABASE_URL from Railway variables if available
if all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    print("🐬 Using Railway MySQL database")
else:
    # Fallback to DATABASE_URL or local development
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Ravish%4099055.@localhost:3306/pfa-b")
    print("🐬 Using local MySQL database")

# For any mysql:// URLs, convert to mysql+pymysql://
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

print(f"Database connection: {MYSQL_HOST or 'localhost'}:{MYSQL_PORT}")

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
