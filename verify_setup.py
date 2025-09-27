#!/usr/bin/env python3
"""Simple test to verify the donation platform setup"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import fastapi
        print("✓ FastAPI imported successfully")
        
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
        
        import pydantic
        print("✓ Pydantic imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_database_setup():
    """Test database connection and model creation"""
    try:
        from database import Base, engine, User, Donation, Need
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Database setup error: {e}")
        return False

def test_app_creation():
    """Test FastAPI app creation"""
    try:
        from main import app
        print("✓ FastAPI app created successfully")
        
        # Check if routes exist
        routes = [route.path for route in app.routes]
        expected_routes = ['/ping', '/donate', '/users/', '/needs/']
        
        for expected in expected_routes:
            if any(expected in route for route in routes):
                print(f"✓ Route {expected} found")
            else:
                print(f"✗ Route {expected} not found")
        
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Donation Platform Setup")
    print("=" * 40)
    
    success = True
    
    success &= test_imports()
    print()
    
    success &= test_database_setup()
    print()
    
    success &= test_app_creation()
    print()
    
    if success:
        print("🎉 All tests passed! The donation platform is ready to run.")
        print("\nTo start the server, run:")
        print("python main.py")
        print("\nThen visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
