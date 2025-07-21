# Configuration file for the Movie Recommendation System
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# TMDB API Configuration
# Get your API key from: https://www.themoviedb.org/settings/api
TMDB_API_KEY = "0ba8f30568bbf5311b7fa9073d56a7f3"

# Database Configuration
DATABASE_FILES = {
    'movies_dict': 'movies_dict.pkl',
    'similarity': 'similarity.pkl'
}

# Vectorization Configuration
VECTORIZER_CONFIG = {
    'max_features': 7500,
    'stop_words': 'english'
}

# Recommendation Configuration
RECOMMENDATION_CONFIG = {
    'top_n': 10
}

# API Configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True
}

# Frontend Configuration
FRONTEND_CONFIG = {
    'host': 'localhost',
    'port': 8501
} 