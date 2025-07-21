#!/usr/bin/env python3
"""
Test script for the Movie Recommendation System
This script tests the backend API endpoints and basic functionality.
"""

import requests
import time
import json

API_BASE_URL = "http://localhost:8000"

def test_backend_connection():
    """Test if the backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            data = response.json()
            print(f"   Total movies: {data['total_movies']}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_get_movies():
    """Test getting all movies"""
    try:
        response = requests.get(f"{API_BASE_URL}/movies", timeout=5)
        if response.status_code == 200:
            movies = response.json()["movies"]
            print(f"✅ Retrieved {len(movies)} movies")
            if movies:
                print(f"   Sample movies: {movies[:5]}")
            return True
        else:
            print(f"❌ Failed to get movies: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting movies: {e}")
        return False

def test_recommendation(movie_name):
    """Test getting recommendations for a movie"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json={"movie_name": movie_name},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Got recommendations for '{movie_name}'")
            print(f"   Found {len(result['recommendations'])} recommendations")
            for i, (movie, score) in enumerate(zip(result['recommendations'], result['similarity_scores'])):
                print(f"   {i+1}. {movie} (similarity: {score:.3f})")
            return True
        else:
            print(f"❌ Failed to get recommendations: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return False

def test_new_movie_addition():
    """Test adding a new movie (requires TMDB API key)"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json={"movie_name": "The Matrix Reloaded"},
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully added new movie and got recommendations")
            print(f"   Movie: {result['movie_name']}")
            print(f"   Recommendations: {len(result['recommendations'])}")
            return True
        elif response.status_code == 404:
            print("⚠️  Movie not found (TMDB API key may not be set)")
            return True
        else:
            print(f"❌ Failed to add new movie: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing new movie addition: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Movie Recommendation System")
    print("=" * 40)
    
    # Test 1: Backend connection
    print("\n1. Testing backend connection...")
    if not test_backend_connection():
        print("❌ Backend tests failed. Please start the backend first.")
        return
    
    # Test 2: Get movies
    print("\n2. Testing movie retrieval...")
    if not test_get_movies():
        print("❌ Movie retrieval failed.")
        return
    
    # Test 3: Get recommendations for existing movie
    print("\n3. Testing recommendations for existing movie...")
    if not test_recommendation("Batman Begins"):
        print("❌ Recommendation test failed.")
        return
    
    # Test 4: Test new movie addition
    print("\n4. Testing new movie addition...")
    test_new_movie_addition()
    
    print("\n✅ All tests completed!")
    print("\n🎬 Your Movie Recommendation System is working correctly!")
    print("   Frontend: http://localhost:8501")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 