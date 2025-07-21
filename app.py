import streamlit as st
<<<<<<< HEAD
import pickle
import pandas as pd

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)

    st.write('### Recommended Movies')
    for i, movie in enumerate(recommended_movies):
        st.write(f'{i+1}. {movie}')

movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie do you like best?',
    movies['title'].values
)

if st.button('Recommend'):
    recommend(selected_movie_name)
=======

st.set_page_config(
    page_title="Movie Recommendation System - Legacy",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.markdown("---")

st.warning("""
## ⚠️ This is the legacy version

The application has been restructured into a full-stack system with FastAPI backend and Streamlit frontend.

### 🚀 To run the new version:

**Option 1: Use the startup script (Recommended)**
```bash
python run_app.py
```

**Option 2: Start components separately**
```bash
# Terminal 1: Start backend
python start_backend.py

# Terminal 2: Start frontend  
python start_frontend.py
```

### 📁 New Project Structure:
```
├── backend/          # FastAPI backend
├── frontend/         # Streamlit frontend
├── run_app.py        # Startup script
├── start_backend.py  # Backend only
└── start_frontend.py # Frontend only
```

### 🌐 Access Points:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### ✨ New Features:
- **5000+ movies** in initial database
- **Dynamic movie addition** via TMDB API
- **Real-time similarity updates**
- **RESTful API** with FastAPI
- **Modern UI** with Streamlit
""")

st.info("""
### 📖 For more information, see the updated README.md file.
""")

def get_recommendations(movie_name, top_n=10):
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
    similar_indices = np.argsort(distances)[::-1]
    similar_indices = [idx for idx in similar_indices if idx != movie_index][:top_n]

    recommendations = []
    similarity_scores = []

    for idx in similar_indices:
        recommendations.append(movies_df.iloc[idx]['title'])
        similarity_scores.append(float(distances[idx]))

    # Debug: print similarity scores
    print(f"Recommendations for '{movie_name}':")
    for title, score in zip(recommendations, similarity_scores):
        print(f"  {title}: {score:.3f}")

    return recommendations, similarity_scores
>>>>>>> d9092e05 (Full Stack Changes - Integrated TMDBAPI using FastAPI for realtime movie recommendations)
