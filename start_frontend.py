#!/usr/bin/env python3
"""
Start the Streamlit frontend
"""

import os
import sys
import subprocess
import requests
import time

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start the backend first:")
        print("   python start_backend.py")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎬 Starting Streamlit frontend...")
    
    if not check_backend():
        return
    
    try:
        os.chdir("frontend")
        print("🌐 Frontend will be available at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501", "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
    finally:
        os.chdir("..")

if __name__ == "__main__":
    start_frontend() 