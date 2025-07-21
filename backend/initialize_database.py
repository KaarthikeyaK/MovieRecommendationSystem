import pandas as pd
import numpy as np
import pickle
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def convert(batch):
    """Convert JSON string to list of names"""
    L = []
    try:
        for i in ast.literal_eval(batch):
            L.append(i['name'])
    except:
        pass
    return L

def convert_cast(batch):
    """Convert cast JSON to list of top 3 cast members"""
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(batch):
            if counter < 3:
                L.append(i['name'])
                counter += 1
            else:
                break
    except:
        pass
    return L

def convert_crew(batch):
    """Convert crew JSON to list of directors"""
    L = []
    try:
        for i in ast.literal_eval(batch):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
    except:
        pass
    return L

def stem(text):
    """Apply stemming to text"""
    ps = PorterStemmer()
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def initialize_database():
    """Initialize the movie database with the 5000 movies from CSV files"""
    print("Loading movie data...")
    
    # Load CSV files
    movies = pd.read_csv('../Datasets/tmdb_5000_movies.csv')
    credits = pd.read_csv('../Datasets/tmdb_5000_credits.csv')
    
    print(f"Loaded {len(movies)} movies and {len(credits)} credits")
    
    # Merge datasets
    movies = movies.merge(credits, on='title')
    print(f"After merging: {len(movies)} movies")
    
    # Select required columns
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    
    # Drop movies without overview
    movies.dropna(inplace=True)
    print(f"After dropping nulls: {len(movies)} movies")
    
    # Convert JSON columns to lists
    print("Converting JSON columns...")
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(convert_crew)
    
    # Convert overview to list
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    # Remove spaces from names
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    
    # Create tags
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    # Create final dataframe
    new_df = movies[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
    
    # Apply stemming
    print("Applying stemming...")
    new_df['tags'] = new_df['tags'].apply(stem)
    
    # Vectorization
    print("Creating vectors...")
    cv = CountVectorizer(max_features=7500, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    
    # Calculate similarity matrix
    print("Calculating similarity matrix...")
    similarity = cosine_similarity(vectors)
    
    # Save to pickle files
    print("Saving to pickle files...")
    pickle.dump(new_df.to_dict(), open('movies_dict.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))
    
    print(f"Database initialized with {len(new_df)} movies")
    print("Files saved: movies_dict.pkl, similarity.pkl")
    
    # Test recommendation
    print("\nTesting recommendation for 'Batman Begins'...")
    movie_index = new_df[new_df.title == 'Batman Begins'].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    print("Top 10 recommendations:")
    for i, (idx, score) in enumerate(movies_list):
        print(f"{i+1}. {new_df.iloc[idx].title} (similarity: {score:.3f})")

if __name__ == "__main__":
    initialize_database() 