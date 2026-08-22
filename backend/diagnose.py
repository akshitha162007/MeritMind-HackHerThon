#!/usr/bin/env python3
"""Diagnostic script to test backend connectivity and database setup."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_env():
    """Test environment variables."""
    print("=" * 60)
    print("TESTING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
    
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Mask password
        masked = db_url.replace(db_url.split("@")[0].split("://")[1], "***:***")
        print(f"✓ DATABASE_URL: {masked}")
    else:
        print("✗ DATABASE_URL: NOT SET")
        return False
    
    return True

def test_database():
    """Test database connection."""
    print("\n" + "=" * 60)
    print("TESTING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        from database import engine, SessionLocal
        
        print("Testing connection...")
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")
        
        print("Testing session...")
        db = SessionLocal()
        db.close()
        print("✓ Database session successful")
        
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test model imports."""
    print("\n" + "=" * 60)
    print("TESTING MODEL IMPORTS")
    print("=" * 60)
    
    try:
        from models import User, Session, JobDescription, BiasReport
        print("✓ Models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Model import failed: {e}")
        return False

def test_tables():
    """Test table creation."""
    print("\n" + "=" * 60)
    print("TESTING TABLE CREATION")
    print("=" * 60)
    
    try:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created/verified successfully")
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        return False

def test_auth():
    """Test authentication functions."""
    print("\n" + "=" * 60)
    print("TESTING AUTHENTICATION")
    print("=" * 60)
    
    try:
        import bcrypt
        test_pwd = "testpassword123"
        hashed = bcrypt.hashpw(test_pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        verified = bcrypt.checkpw(test_pwd.encode('utf-8'), hashed.encode('utf-8'))
        if verified:
            print("✓ Password hashing and verification working")
            return True
        else:
            print("✗ Password verification failed")
            return False
    except Exception as e:
        print(f"✗ Auth test failed: {e}")
        return False

def test_api():
    """Test API startup."""
    print("\n" + "=" * 60)
    print("TESTING API IMPORT")
    print("=" * 60)
    
    try:
        from main import app
        print("✓ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"✗ API import failed: {e}")
        return False

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  MERIT MIND BACKEND DIAGNOSTIC TOOL".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    results.append(("Environment", test_env()))
    results.append(("Database", test_database()))
    results.append(("Models", test_models()))
    results.append(("Tables", test_tables()))
    results.append(("Auth", test_auth()))
    results.append(("API", test_api()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20} {status}")
    
    print("=" * 60)
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! Backend is ready to run.")
        print("\nStart the backend with:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        sys.exit(1)
