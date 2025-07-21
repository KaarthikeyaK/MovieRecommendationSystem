from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import requests
import json
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = FastAPI(title="Movie Recommendation API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
movies_df = None
similarity_matrix = None
vectorizer = None
ps = PorterStemmer()

class MovieRequest(BaseModel):
    movie_name: str

class MovieResponse(BaseModel):
    movie_name: str
    recommendations: list
    similarity_scores: list

def load_movie_data():
    """Load movie data and similarity matrix"""
    global movies_df, similarity_matrix, vectorizer
    
    # Load pickle files if they exist
    if os.path.exists('movies_dict.pkl') and os.path.exists('similarity.pkl'):
        movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies_df = pd.DataFrame(movie_dict)
        similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
        
        # Recreate vectorizer for new movies
        vectorizer = CountVectorizer(max_features=7500, stop_words='english')
        vectors = vectorizer.fit_transform(movies_df['tags']).toarray()
        print(f"Loaded {len(movies_df)} movies from pickle files")
    else:
        # Initialize empty dataframe if no pickle files
        movies_df = pd.DataFrame(columns=['movie_id', 'title', 'tags'])
        similarity_matrix = np.array([])
        vectorizer = CountVectorizer(max_features=7500, stop_words='english')
        print("No pickle files found. Starting with empty database.")

def stem(text):
    """Apply stemming to text"""
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def convert_json_to_list(json_str):
    """Convert JSON string to list of names"""
    try:
        data = ast.literal_eval(json_str)
        return [item['name'] for item in data]
    except:
        return []

def convert_cast_to_list(json_str):
    """Convert cast JSON to list of top 3 cast members"""
    try:
        data = ast.literal_eval(json_str)
        cast_list = []
        for i, item in enumerate(data):
            if i < 3:
                cast_list.append(item['name'])
            else:
                break
        return cast_list
    except:
        return []

def convert_crew_to_list(json_str):
    """Convert crew JSON to list of directors"""
    try:
        data = ast.literal_eval(json_str)
        directors = []
        for item in data:
            if item['job'] == 'Director':
                directors.append(item['name'])
                break
        return directors
    except:
        return []

def fetch_movie_from_tmdb(movie_name):
    """Fetch movie data from TMDB API"""
    from config import TMDB_API_KEY
    
    if TMDB_API_KEY == "your_tmdb_api_key_here":
        print("Warning: Please set your TMDB API key in backend/config.py")
        return None
    
    # Search for movie
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'language': 'en-US',
        'page': 1
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        if not search_results['results']:
            return None
        
        movie = search_results['results'][0]
        movie_id = movie['id']
        
        # Get detailed movie info
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        movie_params = {
            'api_key': TMDB_API_KEY,
            'append_to_response': 'credits'
        }
        
        movie_response = requests.get(movie_url, params=movie_params)
        movie_response.raise_for_status()
        movie_data = movie_response.json()
        
        # Extract required information
        overview = movie_data.get('overview', '')
        genres = [genre['name'] for genre in movie_data.get('genres', [])]
        keywords = [keyword['name'] for keyword in movie_data.get('keywords', {}).get('keywords', [])]
        cast = [person['name'] for person in movie_data.get('credits', {}).get('cast', [])[:3]]
        crew = [person['name'] for person in movie_data.get('credits', {}).get('crew', []) if person['job'] == 'Director']
        
        return {
            'movie_id': movie_id,
            'title': movie_data['title'],
            'overview': overview,
            'genres': genres,
            'keywords': keywords,
            'cast': cast,
            'crew': crew
        }
    except Exception as e:
        print(f"Error fetching movie from TMDB: {e}")
        return None

def add_movie_to_database(movie_data):
    """Add a new movie to the database and update similarity matrix"""
    global movies_df, similarity_matrix, vectorizer
    
    # Process movie data
    overview_words = movie_data['overview'].split()
    genres = [genre.replace(" ", "") for genre in movie_data['genres']]
    keywords = [keyword.replace(" ", "") for keyword in movie_data['keywords']]
    cast = [person.replace(" ", "") for person in movie_data['cast']]
    crew = [person.replace(" ", "") for person in movie_data['crew']]
    
    # Create tags
    tags = overview_words + genres + keywords + cast + crew
    tags_text = " ".join(tags).lower()
    tags_stemmed = stem(tags_text)
    
    # Add to dataframe
    new_movie = pd.DataFrame({
        'movie_id': [movie_data['movie_id']],
        'title': [movie_data['title']],
        'tags': [tags_stemmed]
    })
    
    movies_df = pd.concat([movies_df, new_movie], ignore_index=True)
    
    # Update similarity matrix
    vectors = vectorizer.fit_transform(movies_df['tags']).toarray()
    similarity_matrix = cosine_similarity(vectors)
    
    # Save updated data
    pickle.dump(movies_df.to_dict(), open('movies_dict.pkl', 'wb'))
    pickle.dump(similarity_matrix, open('similarity.pkl', 'wb'))
    
    return len(movies_df) - 1  # Return the index of the new movie

def get_recommendations(movie_name, top_n=10):
    """Get movie recommendations"""
    global movies_df, similarity_matrix
    
    if movies_df.empty:
        return [], []
    
    # Find movie index
    movie_indices = movies_df[movies_df['title'].str.lower() == movie_name.lower()].index
    
    if len(movie_indices) == 0:
        return [], []
    
    movie_index = movie_indices[0]
    distances = similarity_matrix[movie_index]
    
    # Get top N similar movies (excluding itself)
    similar_indices = np.argsort(distances)[::-1][1:top_n+1]
    
    recommendations = []
    similarity_scores = []
    
    for idx in similar_indices:
        recommendations.append(movies_df.iloc[idx]['title'])
        similarity_scores.append(float(distances[idx]))
    
    return recommendations, similarity_scores

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    load_movie_data()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Movie Recommendation API", "total_movies": len(movies_df) if movies_df is not None else 0}

@app.get("/movies")
async def get_all_movies():
    """Get all movies in the database"""
    if movies_df is None:
        return {"movies": []}
    return {"movies": movies_df['title'].tolist()}

@app.post("/recommend", response_model=MovieResponse)
async def recommend_movies(request: MovieRequest):
    """Get movie recommendations"""
    movie_name = request.movie_name
    
    # Check if movie exists in database
    if movies_df is not None and not movies_df.empty:
        movie_exists = movies_df[movies_df['title'].str.lower() == movie_name.lower()].shape[0] > 0
    else:
        movie_exists = False
    
    if not movie_exists:
        # Fetch movie from TMDB API
        movie_data = fetch_movie_from_tmdb(movie_name)
        if movie_data is None:
            raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found in database or TMDB API")
        
        # Add to database
        add_movie_to_database(movie_data)
        print(f"Added new movie: {movie_name}")
    
    # Get recommendations
    recommendations, similarity_scores = get_recommendations(movie_name)
    
    return MovieResponse(
        movie_name=movie_name,
        recommendations=recommendations,
        similarity_scores=similarity_scores
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "total_movies": len(movies_df) if movies_df is not None else 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 