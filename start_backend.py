#!/usr/bin/env python3
"""
Start the FastAPI backend server
"""

import os
import sys
import subprocess
import time
import requests

def check_database():
    """Check if database files exist"""
    if not os.path.exists("backend/movies_dict.pkl") or not os.path.exists("backend/similarity.pkl"):
        print("⚠️  Database files not found. Initializing database...")
        os.chdir("backend")
        result = subprocess.run([sys.executable, "initialize_database.py"], 
                              capture_output=True, text=True)
        os.chdir("..")
        
        if result.returncode != 0:
            print("❌ Database initialization failed")
            return False
        
        print("✅ Database initialized successfully")
    else:
        print("✅ Database files found")
    
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend...")
    
    if not check_database():
        return
    
    try:
        os.chdir("backend")
        print("📡 Backend will be available at: http://localhost:8000")
        print("📚 API documentation at: http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
    finally:
        os.chdir("..")

if __name__ == "__main__":
    start_backend() 