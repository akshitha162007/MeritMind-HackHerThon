#!/usr/bin/env python3
"""Enhanced health check script for Merit Mind backend."""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))

def get_system_info():
    """Get system information."""
    import platform
    import psutil
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "disk_free": psutil.disk_usage('.').free
    }

def check_database_detailed():
    """Detailed database check."""
    try:
        from database import engine, SessionLocal
        from models import User, JobDescription, BiasReport
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT version()").fetchone()
            db_version = result[0] if result else "Unknown"
        
        # Test session and queries
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            jd_count = db.query(JobDescription).count()
            bias_count = db.query(BiasReport).count()
        finally:
            db.close()
        
        return {
            "status": "healthy",
            "database_version": db_version,
            "user_count": user_count,
            "job_description_count": jd_count,
            "bias_report_count": bias_count,
            "connection_pool_size": engine.pool.size(),
            "checked_out_connections": engine.pool.checkedout()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

def check_api_endpoints():
    """Check if API endpoints are accessible."""
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        health_response = client.get("/api/health")
        
        # Test auth endpoints (should return 400/401, not 500)
        register_response = client.post("/api/auth/register", json={})
        login_response = client.post("/api/auth/login", json={})
        
        return {
            "status": "healthy",
            "health_endpoint": health_response.status_code == 200,
            "register_endpoint": register_response.status_code in [400, 422],
            "login_endpoint": login_response.status_code in [400, 422],
            "total_routes": len(app.routes)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "fastapi", "uvicorn", "sqlalchemy", "psycopg2-binary",
        "bcrypt", "python-dotenv", "pydantic", "openai"
    ]
    
    installed = {}
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            installed[package] = "✓"
        except ImportError:
            installed[package] = "✗"
            missing.append(package)
    
    return {
        "status": "healthy" if not missing else "unhealthy",
        "installed_packages": installed,
        "missing_packages": missing
    }

def check_environment():
    """Check environment variables and configuration."""
    required_vars = ["DATABASE_URL"]
    optional_vars = ["OPENAI_API_KEY", "GROQ_API_KEY"]
    
    env_status = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive data
            if "password" in value.lower() or "key" in var.lower():
                masked = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
                env_status[var] = f"Set ({masked})"
            else:
                env_status[var] = "Set"
        else:
            env_status[var] = "Missing"
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
            env_status[var] = f"Set ({masked})"
        else:
            env_status[var] = "Not set (optional)"
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    
    return {
        "status": "healthy" if not missing_required else "unhealthy",
        "environment_variables": env_status,
        "missing_required": missing_required
    }

def generate_health_report():
    """Generate comprehensive health report."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": "unknown",
        "checks": {}
    }
    
    # Run all checks
    checks = {
        "system": get_system_info,
        "environment": check_environment,
        "dependencies": check_dependencies,
        "database": check_database_detailed,
        "api": check_api_endpoints
    }
    
    healthy_checks = 0
    total_checks = len(checks)
    
    for check_name, check_func in checks.items():
        try:
            result = check_func()
            report["checks"][check_name] = result
            if result.get("status") == "healthy" or check_name == "system":
                healthy_checks += 1
        except Exception as e:
            report["checks"][check_name] = {
                "status": "error",
                "error": str(e)
            }
    
    # Determine overall status
    if healthy_checks == total_checks:
        report["overall_status"] = "healthy"
    elif healthy_checks >= total_checks * 0.7:
        report["overall_status"] = "degraded"
    else:
        report["overall_status"] = "unhealthy"
    
    return report

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("MERIT MIND COMPREHENSIVE HEALTH CHECK".center(70))
    print("=" * 70 + "\n")
    
    report = generate_health_report()
    
    # Print summary
    status_color = {
        "healthy": "✓",
        "degraded": "⚠",
        "unhealthy": "✗",
        "unknown": "?"
    }
    
    print(f"Overall Status: {status_color.get(report['overall_status'], '?')} {report['overall_status'].upper()}")
    print(f"Timestamp: {report['timestamp']}")
    print()
    
    # Print detailed results
    for check_name, result in report["checks"].items():
        status = result.get("status", "unknown")
        print(f"{check_name.title()} Check: {status_color.get(status, '?')} {status.upper()}")
        
        if status == "unhealthy" and "error" in result:
            print(f"  Error: {result['error']}")
        elif status == "unhealthy" and "missing_required" in result:
            print(f"  Missing: {', '.join(result['missing_required'])}")
        elif status == "unhealthy" and "missing_packages" in result:
            print(f"  Missing packages: {', '.join(result['missing_packages'])}")
        
        # Show additional details for some checks
        if check_name == "database" and status == "healthy":
            print(f"  Users: {result.get('user_count', 0)}")
            print(f"  Job Descriptions: {result.get('job_description_count', 0)}")
            print(f"  Bias Reports: {result.get('bias_report_count', 0)}")
        elif check_name == "api" and status == "healthy":
            print(f"  Total Routes: {result.get('total_routes', 0)}")
        
        print()
    
    # Save detailed report
    report_file = Path(__file__).parent / "health_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Detailed report saved to: {report_file}")
    
    # Recommendations
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    if report["overall_status"] == "healthy":
        print("✓ System is healthy and ready to run!")
        print("  Start backend: python start.py")
        print("  Start frontend: npm run dev")
    elif report["overall_status"] == "degraded":
        print("⚠ System has some issues but may still work:")
        print("  Check the failed checks above")
        print("  Consider fixing issues for better performance")
    else:
        print("✗ System has critical issues:")
        print("  Fix the failed checks above before starting")
        print("  Check LOGIN_SIGNUP_TROUBLESHOOTING.md for help")
    
    print("\n" + "=" * 70)
    
    return 0 if report["overall_status"] in ["healthy", "degraded"] else 1

if __name__ == "__main__":
    sys.exit(main())