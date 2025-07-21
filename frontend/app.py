import streamlit as st
import requests
import pandas as pd
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

def get_all_movies():
    """Get all movies from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/movies")
        if response.status_code == 200:
            return response.json()["movies"]
        else:
            st.error(f"Error fetching movies: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the backend is running.")
        return []

def get_recommendations(movie_name):
    """Get movie recommendations from the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json={"movie_name": movie_name}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting recommendations: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the backend is running.")
        return None

def main():
    st.set_page_config(
        page_title="Movie Recommendation System",
        page_icon="🎬",
        layout="wide"
    )
    
    # Header
    st.title("🎬 Movie Recommendation System")
    st.markdown("---")
    
    # Sidebar for API status
    with st.sidebar:
        st.header("API Status")
        try:
            health_response = requests.get(f"{API_BASE_URL}/health")
            if health_response.status_code == 200:
                health_data = health_response.json()
                st.success("✅ Backend Connected")
                st.info(f"Total Movies: {health_data['total_movies']}")
            else:
                st.error("❌ Backend Error")
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend Not Connected")
            st.info("Please start the backend server first")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Find Your Next Favorite Movie")
        
        # Movie selection
        movies = get_all_movies()
        
        if movies:
            selected_movie = st.selectbox(
                "Choose a movie you like:",
                movies,
                index=0 if movies else None
            )
            
            # Custom movie input
            st.markdown("---")
            st.subheader("Or enter a custom movie:")
            custom_movie = st.text_input(
                "Enter movie name:",
                placeholder="e.g., The Matrix, Inception, etc."
            )
            
            # Recommendation button
            if st.button("🎯 Get Recommendations", type="primary"):
                movie_to_search = custom_movie if custom_movie else selected_movie
                
                if movie_to_search:
                    with st.spinner("Finding similar movies..."):
                        result = get_recommendations(movie_to_search)
                        
                        if result:
                            st.success(f"Found recommendations for: **{result['movie_name']}**")
                            
                            # Display recommendations
                            st.markdown("### 🎬 Recommended Movies")
                            
                            for i, (movie, score) in enumerate(zip(result['recommendations'], result['similarity_scores'])):
                                with st.container():
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        st.markdown(f"**{i+1}. {movie}**")
                                    with col_b:
                                        st.metric("Similarity", f"{score:.3f}")
                                    st.divider()
        else:
            st.warning("No movies available. Please check if the backend is running and the database is initialized.")
    
    with col2:
        st.header("How it works")
        st.markdown("""
        1. **Choose a movie** from the dropdown or enter a custom movie name
        2. **Click 'Get Recommendations'** to find similar movies
        3. **New movies** not in our database will be automatically fetched from TMDB API
        4. **Similarity scores** show how close each recommendation is to your chosen movie
        """)
        
        st.markdown("---")
        st.header("Features")
        st.markdown("""
        ✅ **5000+ movies** in the initial database
        ✅ **Dynamic addition** of new movies via TMDB API
        ✅ **Cosine similarity** based recommendations
        ✅ **Real-time** similarity matrix updates
        ✅ **FastAPI backend** with RESTful API
        """)

if __name__ == "__main__":
    main() 