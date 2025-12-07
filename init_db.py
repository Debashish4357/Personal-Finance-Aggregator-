#!/usr/bin/env python3
"""
Database initialization script for Railway deployment
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def init_database():
    """Initialize database tables"""
    try:
        print("Initializing database...")
        
        # Import after setting up the path
        from db.database import engine
        from schema.models import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Check if we're on Railway (MySQL)
        database_url = os.getenv("DATABASE_URL", "")
        if "railway" in database_url.lower() or database_url.startswith("mysql://"):
            print("🐬 Using MySQL database (Railway)")
        else:
            print("🐬 Using MySQL database (Local)")
            
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)