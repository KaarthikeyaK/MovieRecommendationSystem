#!/usr/bin/env python3
"""
Movie Recommendation System - Startup Script
This script initializes the database and starts the full-stack application.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        import pandas
        import numpy
        import sklearn
        import nltk
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database with the 5000 movies"""
    print("🔧 Initializing database...")
    
    # Check if pickle files already exist
    if os.path.exists("backend/movies_dict.pkl") and os.path.exists("backend/similarity.pkl"):
        print("✅ Database already initialized")
        return True
    
    # Run the initialization script
    try:
        os.chdir("backend")
        result = subprocess.run([sys.executable, "initialize_database.py"], 
                              capture_output=True, text=True)
        os.chdir("..")
        
        if result.returncode == 0:
            print("✅ Database initialized successfully")
            return True
        else:
            print(f"❌ Database initialization failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend...")
    
    try:
        os.chdir("backend")
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        os.chdir("..")
        
        # Wait for backend to start
        print("⏳ Waiting for backend to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is running on http://localhost:8000")
                    return backend_process
            except requests.exceptions.RequestException:
                time.sleep(1)
                continue
        
        print("❌ Backend failed to start")
        return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎬 Starting Streamlit frontend...")
    
    try:
        os.chdir("frontend")
        # Start frontend
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501", "--server.address", "localhost"
        ])
        os.chdir("..")
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main startup function"""
    print("🎬 Movie Recommendation System")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Initialize database
    if not initialize_database():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    try:
        # Start frontend
        start_frontend()
    finally:
        # Cleanup
        if backend_process:
            print("🛑 Stopping backend...")
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
    main() 