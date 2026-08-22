#!/usr/bin/env python3
"""Automated testing script for login/signup functionality."""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

def test_auth_endpoints():
    """Test authentication endpoints."""
    print("\n" + "=" * 70)
    print("TESTING AUTHENTICATION ENDPOINTS")
    print("=" * 70 + "\n")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        test_results = []
        
        # Test 1: Health Check
        print("[1/6] Testing health endpoint...")
        start = time.time()
        response = client.get("/api/health")
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✓ Health check passed ({elapsed:.2f}s)")
            test_results.append(("Health Check", True, elapsed))
        else:
            print(f"✗ Health check failed (status: {response.status_code})")
            test_results.append(("Health Check", False, elapsed))
        
        # Test 2: Register with valid data
        print("[2/6] Testing registration with valid data...")
        start = time.time()
        register_data = {
            "name": "Test User",
            "email": f"test_{int(time.time())}@example.com",
            "password": "password123",
            "role": "recruiter"
        }
        response = client.post("/api/auth/register", json=register_data)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user_id" in data:
                print(f"✓ Registration passed ({elapsed:.2f}s)")
                test_results.append(("Registration", True, elapsed))
                token = data["token"]
                user_id = data["user_id"]
            else:
                print(f"✗ Registration response missing fields")
                test_results.append(("Registration", False, elapsed))
                token = None
        else:
            print(f"✗ Registration failed (status: {response.status_code})")
            print(f"  Response: {response.text}")
            test_results.append(("Registration", False, elapsed))
            token = None
        
        # Test 3: Register with duplicate email
        print("[3/6] Testing duplicate email rejection...")
        start = time.time()
        response = client.post("/api/auth/register", json=register_data)
        elapsed = time.time() - start
        
        if response.status_code == 409:
            print(f"✓ Duplicate email rejected ({elapsed:.2f}s)")
            test_results.append(("Duplicate Email Check", True, elapsed))
        else:
            print(f"✗ Duplicate email not rejected (status: {response.status_code})")
            test_results.append(("Duplicate Email Check", False, elapsed))
        
        # Test 4: Login with valid credentials
        print("[4/6] Testing login with valid credentials...")
        start = time.time()
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user_id" in data:
                print(f"✓ Login passed ({elapsed:.2f}s)")
                test_results.append(("Login", True, elapsed))
                login_token = data["token"]
            else:
                print(f"✗ Login response missing fields")
                test_results.append(("Login", False, elapsed))
                login_token = None
        else:
            print(f"✗ Login failed (status: {response.status_code})")
            print(f"  Response: {response.text}")
            test_results.append(("Login", False, elapsed))
            login_token = None
        
        # Test 5: Login with invalid password
        print("[5/6] Testing login with invalid password...")
        start = time.time()
        invalid_login = {
            "email": register_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=invalid_login)
        elapsed = time.time() - start
        
        if response.status_code == 401:
            print(f"✓ Invalid password rejected ({elapsed:.2f}s)")
            test_results.append(("Invalid Password Check", True, elapsed))
        else:
            print(f"✗ Invalid password not rejected (status: {response.status_code})")
            test_results.append(("Invalid Password Check", False, elapsed))
        
        # Test 6: Logout
        print("[6/6] Testing logout...")
        if login_token:
            start = time.time()
            response = client.post(
                "/api/auth/logout",
                json={"token": login_token}
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                print(f"✓ Logout passed ({elapsed:.2f}s)")
                test_results.append(("Logout", True, elapsed))
            else:
                print(f"✗ Logout failed (status: {response.status_code})")
                test_results.append(("Logout", False, elapsed))
        else:
            print("⊘ Logout skipped (no token available)")
            test_results.append(("Logout", None, 0))
        
        return test_results
    
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return []

def test_database_operations():
    """Test database operations."""
    print("\n" + "=" * 70)
    print("TESTING DATABASE OPERATIONS")
    print("=" * 70 + "\n")
    
    try:
        from database import SessionLocal
        from models import User
        
        test_results = []
        
        # Test 1: Create user
        print("[1/3] Testing user creation...")
        start = time.time()
        db = SessionLocal()
        try:
            user = User(
                name="DB Test User",
                email=f"dbtest_{int(time.time())}@example.com",
                password_hash="test_hash",
                role="candidate"
            )
            db.add(user)
            db.commit()
            elapsed = time.time() - start
            print(f"✓ User creation passed ({elapsed:.2f}s)")
            test_results.append(("User Creation", True, elapsed))
            user_id = user.id
        except Exception as e:
            elapsed = time.time() - start
            print(f"✗ User creation failed: {e}")
            test_results.append(("User Creation", False, elapsed))
            user_id = None
        finally:
            db.close()
        
        # Test 2: Query user
        print("[2/3] Testing user query...")
        if user_id:
            start = time.time()
            db = SessionLocal()
            try:
                queried_user = db.query(User).filter(User.id == user_id).first()
                elapsed = time.time() - start
                if queried_user:
                    print(f"✓ User query passed ({elapsed:.2f}s)")
                    test_results.append(("User Query", True, elapsed))
                else:
                    print(f"✗ User not found")
                    test_results.append(("User Query", False, elapsed))
            except Exception as e:
                elapsed = time.time() - start
                print(f"✗ User query failed: {e}")
                test_results.append(("User Query", False, elapsed))
            finally:
                db.close()
        else:
            print("⊘ User query skipped (no user created)")
            test_results.append(("User Query", None, 0))
        
        # Test 3: Count users
        print("[3/3] Testing user count...")
        start = time.time()
        db = SessionLocal()
        try:
            count = db.query(User).count()
            elapsed = time.time() - start
            print(f"✓ User count passed ({elapsed:.2f}s) - Total users: {count}")
            test_results.append(("User Count", True, elapsed))
        except Exception as e:
            elapsed = time.time() - start
            print(f"✗ User count failed: {e}")
            test_results.append(("User Count", False, elapsed))
        finally:
            db.close()
        
        return test_results
    
    except Exception as e:
        print(f"✗ Error during database testing: {e}")
        return []

def test_password_hashing():
    """Test password hashing and verification."""
    print("\n" + "=" * 70)
    print("TESTING PASSWORD HASHING")
    print("=" * 70 + "\n")
    
    try:
        import bcrypt
        
        test_results = []
        
        # Test 1: Hash password
        print("[1/3] Testing password hashing...")
        start = time.time()
        password = "TestPassword123!"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        elapsed = time.time() - start
        print(f"✓ Password hashing passed ({elapsed:.2f}s)")
        test_results.append(("Password Hashing", True, elapsed))
        
        # Test 2: Verify correct password
        print("[2/3] Testing password verification (correct)...")
        start = time.time()
        verified = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        elapsed = time.time() - start
        if verified:
            print(f"✓ Password verification passed ({elapsed:.2f}s)")
            test_results.append(("Password Verification", True, elapsed))
        else:
            print(f"✗ Password verification failed")
            test_results.append(("Password Verification", False, elapsed))
        
        # Test 3: Reject wrong password
        print("[3/3] Testing password verification (wrong)...")
        start = time.time()
        wrong_password = "WrongPassword123!"
        verified = bcrypt.checkpw(wrong_password.encode('utf-8'), hashed.encode('utf-8'))
        elapsed = time.time() - start
        if not verified:
            print(f"✓ Wrong password rejected ({elapsed:.2f}s)")
            test_results.append(("Wrong Password Rejection", True, elapsed))
        else:
            print(f"✗ Wrong password not rejected")
            test_results.append(("Wrong Password Rejection", False, elapsed))
        
        return test_results
    
    except Exception as e:
        print(f"✗ Error during password testing: {e}")
        return []

def generate_test_report(all_results):
    """Generate test report."""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70 + "\n")
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    skipped_tests = 0
    total_time = 0
    
    for test_name, result, elapsed in all_results:
        total_tests += 1
        total_time += elapsed
        
        if result is True:
            passed_tests += 1
            status = "✓ PASS"
        elif result is False:
            failed_tests += 1
            status = "✗ FAIL"
        else:
            skipped_tests += 1
            status = "⊘ SKIP"
        
        print(f"{test_name:30} {status:10} ({elapsed:.2f}s)")
    
    print("\n" + "-" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Skipped: {skipped_tests}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Success Rate: {(passed_tests / (total_tests - skipped_tests) * 100):.1f}%" if (total_tests - skipped_tests) > 0 else "N/A")
    print("-" * 70)
    
    if failed_tests == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {failed_tests} TEST(S) FAILED")
        return 1

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("MERIT MIND AUTOMATED TEST SUITE".center(70))
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_auth_endpoints())
    all_results.extend(test_database_operations())
    all_results.extend(test_password_hashing())
    
    # Generate report
    exit_code = generate_test_report(all_results)
    
    print(f"Completed: {datetime.now().isoformat()}\n")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
