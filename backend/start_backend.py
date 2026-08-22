#!/usr/bin/env python3
"""
Merit Mind Backend Startup Script
Handles environment setup, database initialization, and server startup
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

def check_environment():
    """Check if all required environment variables are set"""
    print("[*] Checking environment variables...")
    
    required_vars = ["DATABASE_URL", "GROQ_API_KEY"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
        else:
            print(f"  [OK] {var} is set")
    
    if missing:
        print(f"\n[ERROR] Missing environment variables: {', '.join(missing)}")
        print(f"   Please add them to {env_path}")
        return False
    
    return True

def check_database():
    """Test database connection"""
    print("\n[*] Testing database connection...")
    
    try:
        from database import engine
        with engine.connect() as conn:
            print("  [OK] Database connection successful")
            return True
    except Exception as e:
        print(f"  [ERROR] Database connection failed: {e}")
        return False

def init_tables():
    """Initialize database tables"""
    print("\n[*] Initializing database tables...")
    
    try:
        from database import engine
        from models import Base
        Base.metadata.create_all(bind=engine)
        print("  [OK] Tables initialized")
        return True
    except Exception as e:
        print(f"  [ERROR] Table initialization failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n[*] Starting FastAPI server...")
    print("   Server will be available at http://localhost:8000")
    print("   Health check: http://localhost:8000/api/health")
    print("\n   Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            cwd=Path(__file__).resolve().parent
        )
    except KeyboardInterrupt:
        print("\n\n[OK] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")
        sys.exit(1)

def main():
    print("=" * 60)
    print("Merit Mind Backend Startup")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check database
    if not check_database():
        print("\n[WARNING] Database connection failed. Continuing anyway...")
    
    # Initialize tables
    if not init_tables():
        print("\n[WARNING] Table initialization failed. Continuing anyway...")
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
