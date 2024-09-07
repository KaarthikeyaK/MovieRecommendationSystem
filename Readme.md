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