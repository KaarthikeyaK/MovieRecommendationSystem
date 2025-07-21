<<<<<<< HEAD
# Movie Recommendation System

This project is a **Movie Recommendation System** that uses the **TMDB 5000 dataset** and cosine similarity to recommend up to 10 movies based on user preferences. The recommendation system is built in Python and is deployed via a web interface using **Streamlit**.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)

## Project Overview

The Movie Recommendation System utilizes a **content-based filtering** approach, leveraging cosine similarity between movies' features such as genre, keywords, cast, and crew. By providing the name of a movie you like, the system will recommend similar movies from the **TMDB 5000 dataset**.

The entire project is built using **Python**, and the dataframes generated during the data preprocessing are saved as **pickle files** and loaded into the Streamlit-based website.

## Features

- Recommends up to 10 movies based on user input.
- Utilizes cosine similarity for movie recommendations.
- Clean and interactive web interface built with **Streamlit**.
- Easy to use and fast recommendations.

## Dataset

The project uses the **TMDB 5000 Movie Dataset**, which can be found on [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). The dataset contains information on 5000 movies, including metadata like cast, crew, genres, and keywords.

## Technologies Used

- **Python**: Main programming language.
- **Streamlit**: For building the web application.
- **Pandas**: For data manipulation.
- **Pickle**: For serializing and loading dataframes.
- **Cosine Similarity**: For finding similar movies.

## Setup Instructions

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/movie-recommendation-system.git
    cd movie-recommendation-system
    ```

2. **Install Dependencies:**
    Ensure that Python 3.x is installed. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit Web App:**
    To run the web application locally:
    ```bash
    streamlit run app.py
    ```

4. **Download the Dataset:**
   Download the TMDB 5000 dataset from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and place the CSV files in the appropriate directory (e.g., `data/`).

5. **Load Pickle Files:**
   Ensure that the app loads the saved pickle files for quicker recommendations:
   ```python
   import pickle
   movies_df = pickle.load(open('data/movies.pkl', 'rb'))
   ```

## Usage

1. Open the web application by running it via **Streamlit**.
2. Enter the name of a movie you like.
3. The system will recommend up to 10 movies that are similar to the one you entered, based on cosine similarity.
4. Browse through the recommendations and find a movie to watch!
=======
# 🎬 Movie Recommendation System

A full-stack movie recommendation system built with FastAPI backend and Streamlit frontend. The system uses content-based filtering with cosine similarity to recommend movies based on genres, cast, crew, keywords, and overview.

## 🚀 Features

- **5000+ movies** in the initial database
- **Dynamic movie addition** via TMDB API for movies not in the database
- **Real-time similarity matrix updates** when new movies are added
- **Content-based filtering** using cosine similarity
- **FastAPI backend** with RESTful API
- **Streamlit frontend** with modern UI
- **Automatic database initialization** from CSV files

## 📁 Project Structure

```
MovieRecommendationSystem-main/
├── backend/
│   ├── main.py                 # FastAPI backend application
│   └── initialize_database.py  # Database initialization script
├── frontend/
│   └── app.py                  # Streamlit frontend application
├── Datasets/
│   ├── tmdb_5000_movies.csv   # Movie data
│   └── tmdb_5000_credits.csv  # Credits data
├── run_app.py                  # Startup script
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MovieRecommendationSystem-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get TMDB API Key** (optional, for adding new movies)
   - Go to [TMDB API](https://www.themoviedb.org/settings/api)
   - Create an account and get your API key
   - Update the API key in `backend/main.py` (line 108)

## 🚀 Quick Start

### Option 1: Use the startup script (Recommended)
```bash
python run_app.py
```

This will:
- Check dependencies
- Initialize the database with 5000 movies
- Start the FastAPI backend
- Start the Streamlit frontend

### Option 2: Manual startup

1. **Initialize the database**
   ```bash
   cd backend
   python initialize_database.py
   cd ..
   ```

2. **Start the backend**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```

## 🌐 Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 How It Works

### 1. Content-Based Filtering
The system uses the following features to create movie vectors:
- **Overview**: Movie description text
- **Genres**: Movie categories
- **Keywords**: Important tags
- **Cast**: Top 3 actors
- **Crew**: Director information

### 2. Vectorization Process
1. Combine all features into a single text
2. Apply stemming to reduce word variations
3. Create TF-IDF vectors using CountVectorizer
4. Calculate cosine similarity between all movies

### 3. Recommendation Algorithm
1. Find the movie vector in the database
2. Calculate similarity with all other movies
3. Return top 10 most similar movies

### 4. Dynamic Movie Addition
When a movie is not in the database:
1. Fetch movie data from TMDB API
2. Process and vectorize the new movie
3. Add to the similarity matrix
4. Save updated database

## 🔧 API Endpoints

### GET `/`
- Returns API status and total movie count

### GET `/movies`
- Returns list of all movies in the database

### POST `/recommend`
- **Body**: `{"movie_name": "Movie Title"}`
- **Returns**: Movie recommendations with similarity scores

### GET `/health`
- Health check endpoint

## 🎯 Usage Examples

### Using the Frontend
1. Open http://localhost:8501
2. Select a movie from the dropdown or enter a custom movie name
3. Click "Get Recommendations"
4. View the top 10 similar movies with similarity scores

### Using the API directly
```bash
# Get recommendations for "The Matrix"
curl -X POST "http://localhost:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{"movie_name": "The Matrix"}'
```

## 🔍 Database Files

The system creates two pickle files:
- `movies_dict.pkl`: Contains movie data (ID, title, processed tags)
- `similarity.pkl`: Contains the cosine similarity matrix

These files are automatically created during initialization and updated when new movies are added.

## 🛠️ Customization

### Adding TMDB API Key
1. Get your API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Update line 108 in `backend/main.py`:
   ```python
   API_KEY = "your_actual_api_key_here"
   ```

### Modifying Recommendation Algorithm
- Edit the similarity calculation in `backend/main.py`
- Adjust the number of recommendations in the `get_recommendations` function
- Modify the feature weights in the vectorization process

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure the backend is running on port 8000
- Check if the database files exist in the backend directory
- Verify all dependencies are installed

### Database Initialization Issues
- Ensure the CSV files are in the `Datasets/` directory
- Check if you have sufficient disk space for the pickle files
- Verify NLTK data is downloaded

### TMDB API Issues
- Check if your API key is valid
- Ensure you have internet connection
- Verify the API key is correctly set in the backend

## 📈 Performance

- **Initialization**: ~2-3 minutes for 5000 movies
- **Recommendation**: ~100-200ms per request
- **New movie addition**: ~1-2 seconds (including API call)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- TMDB for providing the movie database and API
- Streamlit for the frontend framework
- FastAPI for the backend framework
- Scikit-learn for the machine learning algorithms
>>>>>>> d9092e05 (Full Stack Changes - Integrated TMDBAPI using FastAPI for realtime movie recommendations)
