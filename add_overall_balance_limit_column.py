#!/usr/bin/env python3
"""
Migration script to add overall_balance_limit column to users table
Run this once to update your database schema
"""

from sqlalchemy import text
from db.database import engine

def add_overall_balance_limit_column():
    """Add overall_balance_limit column to users table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'pfa-b' 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'overall_balance_limit'
            """))
            
            count = result.fetchone()[0]
            
            if count == 0:
                # Add the column
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN overall_balance_limit FLOAT NULL
                """))
                conn.commit()
                print("✅ Successfully added 'overall_balance_limit' column to users table")
            else:
                print("ℹ️  Column 'overall_balance_limit' already exists in users table")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nIf you get an error, you can manually run this SQL:")
        print("ALTER TABLE users ADD COLUMN overall_balance_limit FLOAT NULL;")

if __name__ == "__main__":
    print("Adding overall_balance_limit column to users table...")
    add_overall_balance_limit_column()

