#!/usr/bin/env python3
"""
Migration script to create alerts table
Run this once to update your database schema
"""

from sqlalchemy import text
from db.database import engine

def create_alerts_table():
    """Create alerts table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = 'pfa-b' 
                AND TABLE_NAME = 'alerts'
            """))
            
            count = result.fetchone()[0]
            
            if count == 0:
                # Create the table
                conn.execute(text("""
                    CREATE TABLE alerts (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        budget_id INT NULL,
                        alert_type ENUM('BUDGET_80_PERCENT', 'BUDGET_100_PERCENT', 'OVERALL_BALANCE_LIMIT') NOT NULL,
                        message VARCHAR(500) NOT NULL,
                        is_read INT NOT NULL DEFAULT 0,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE,
                        INDEX idx_user_id (user_id),
                        INDEX idx_is_read (is_read)
                    )
                """))
                conn.commit()
                print("✅ Successfully created 'alerts' table")
            else:
                print("ℹ️  Table 'alerts' already exists")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nIf you get an error, you can manually run this SQL:")
        print("""
        CREATE TABLE alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            budget_id INT NULL,
            alert_type ENUM('BUDGET_80_PERCENT', 'BUDGET_100_PERCENT', 'OVERALL_BALANCE_LIMIT') NOT NULL,
            message VARCHAR(500) NOT NULL,
            is_read INT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE
        );
        """)

if __name__ == "__main__":
    print("Creating alerts table...")
    create_alerts_table()

