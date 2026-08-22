#!/usr/bin/env python3
"""Comprehensive setup verification script for Merit Mind."""

import sys
import os
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'=' * 70}")
    print(f"{description}")
    print(f"{'=' * 70}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("MERIT MIND COMPREHENSIVE SETUP VERIFICATION".center(70))
    print("=" * 70)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    results = {}
    
    # Step 1: Environment Check
    print("\n[STEP 1/5] Running environment check...")
    results["environment"] = run_command(
        f"{sys.executable} diagnose.py",
        "ENVIRONMENT CHECK"
    )
    
    # Step 2: Health Check
    print("\n[STEP 2/5] Running health check...")
    results["health"] = run_command(
        f"{sys.executable} health_check.py",
        "COMPREHENSIVE HEALTH CHECK"
    )
    
    # Step 3: Authentication Tests
    print("\n[STEP 3/5] Running authentication tests...")
    results["auth"] = run_command(
        f"{sys.executable} test_auth.py",
        "AUTHENTICATION TESTS"
    )
    
    # Step 4: Performance Monitoring
    print("\n[STEP 4/5] Running performance monitoring...")
    results["performance"] = run_command(
        f"{sys.executable} monitor_performance.py",
        "PERFORMANCE MONITORING"
    )
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY".center(70))
    print("=" * 70 + "\n")
    
    all_passed = True
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check_name.title():20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("\n✓ ALL CHECKS PASSED!")
        print("\nYour Merit Mind backend is ready to run!")
        print("\nNext steps:")
        print("1. Start backend: python start.py")
        print("2. Start frontend: npm run dev")
        print("3. Open: http://localhost:5173")
        return 0
    else:
        print("\n✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above and try again.")
        print("\nFor help, see:")
        print("- LOGIN_SIGNUP_TROUBLESHOOTING.md")
        print("- STARTUP_GUIDE.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
