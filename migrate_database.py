"""
Database Migration Script
Adds badges column to existing users table
Run this once after updating the database schema
"""

import sqlite3
import os

def migrate_database():
    db_file = "donation_platform.db"
    
    if not os.path.exists(db_file):
        print("✅ No existing database found - new schema will be used automatically")
        return
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check if badges column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'badges' not in columns:
            print("🔄 Adding badges column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN badges TEXT DEFAULT ''")
            conn.commit()
            print("✅ Successfully added badges column")
        else:
            print("✅ Badges column already exists")
        
        # Update any users without badges to have empty badges
        cursor.execute("UPDATE users SET badges = '' WHERE badges IS NULL")
        conn.commit()
        
        conn.close()
        print("🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        print("You might need to delete the old database and recreate it.")

if __name__ == "__main__":
    migrate_database()
