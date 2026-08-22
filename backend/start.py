#!/usr/bin/env python3
"""Startup script for Merit Mind backend with database initialization."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("\n" + "=" * 70)
    print("MERIT MIND BACKEND STARTUP".center(70))
    print("=" * 70 + "\n")
    
    # Step 1: Check environment
    print("[1/4] Checking environment variables...")
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("✗ ERROR: DATABASE_URL not set in .env")
        sys.exit(1)
    print("✓ DATABASE_URL configured")
    
    # Step 2: Test database connection
    print("\n[2/4] Testing database connection...")
    try:
        from database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ ERROR: Database connection failed")
        print(f"  {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check DATABASE_URL in .env is correct")
        print("  2. Verify database server is running")
        print("  3. Check network connectivity")
        print("  4. Verify credentials are correct")
        sys.exit(1)
    
    # Step 3: Initialize tables
    print("\n[3/4] Initializing database tables...")
    try:
        from database import Base
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"✗ ERROR: Table initialization failed")
        print(f"  {str(e)}")
        sys.exit(1)
    
    # Step 4: Start API
    print("\n[4/4] Starting FastAPI server...")
    print("\n" + "=" * 70)
    print("Backend is starting on http://0.0.0.0:8000".center(70))
    print("API Documentation: http://localhost:8000/docs".center(70))
    print("=" * 70 + "\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"\n✗ ERROR: Failed to start server")
        print(f"  {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
