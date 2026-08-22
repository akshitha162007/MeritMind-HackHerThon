#!/usr/bin/env python3
"""Test backend connectivity and database setup"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_database():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from database import engine, SessionLocal
        with engine.connect() as conn:
            print("✓ Database connection successful")
        
        # Test session
        db = SessionLocal()
        db.close()
        print("✓ Database session successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test model imports"""
    print("\nTesting model imports...")
    try:
        from models import User, Session, Candidate
        print("✓ Models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Model import failed: {e}")
        return False

def test_tables():
    """Test table creation"""
    print("\nTesting table creation...")
    try:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        return False

def test_auth():
    """Test authentication functions"""
    print("\nTesting authentication functions...")
    try:
        from main import hash_password, verify_password
        test_pwd = "testpassword123"
        hashed = hash_password(test_pwd)
        verified = verify_password(test_pwd, hashed)
        if verified:
            print("✓ Password hashing and verification working")
            return True
        else:
            print("✗ Password verification failed")
            return False
    except Exception as e:
        print(f"✗ Auth test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Merit Mind Backend Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("Database", test_database()))
    results.append(("Models", test_models()))
    results.append(("Tables", test_tables()))
    results.append(("Auth", test_auth()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("=" * 50)
    
    if all_passed:
        print("All tests passed! Backend is ready.")
        sys.exit(0)
    else:
        print("Some tests failed. Check the errors above.")
        sys.exit(1)
