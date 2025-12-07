from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment or use the Railway public URL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:snXHhNeMDFhhHABIuNHPhZPRQDUYhdHA@nozomi.proxy.rlwy.net:49016/railway")

# Convert mysql:// to mysql+pymysql:// for SQLAlchemy compatibility
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    print("🐬 Using Railway MySQL database")
    # Extract host info for display
    host_part = DATABASE_URL.split("@")[1].split("/")[0] if "@" in DATABASE_URL else "unknown"
    print(f"Database connection: {host_part}")
else:
    print("🐬 Using custom MySQL database")

print(f"Connection URL: mysql+pymysql://***@{DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")

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
