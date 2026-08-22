#!/usr/bin/env python3
"""Quick dependency checker"""

import sys

print("Checking dependencies...")
print()

dependencies = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2",
    "bcrypt",
    "python-dotenv",
    "pydantic",
    "vaderSentiment",
    "pdfplumber",
    "pytesseract",
    "openai",
    "groq"
]

missing = []
installed = []

for dep in dependencies:
    try:
        __import__(dep.replace("-", "_"))
        installed.append(dep)
        print(f"[OK] {dep}")
    except ImportError:
        missing.append(dep)
        print(f"[MISSING] {dep}")

print()
print(f"Installed: {len(installed)}/{len(dependencies)}")

if missing:
    print(f"Missing: {', '.join(missing)}")
    print()
    print("Installing missing dependencies...")
    import subprocess
    for dep in missing:
        print(f"  Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", dep])
    print()
    print("All dependencies installed!")
else:
    print("All dependencies are installed!")

print()
print("You can now start the backend with:")
print("  python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
