
import streamlit as st
import pickle
import pandas as pd 
import requests

def fetch_poster_and_description(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=41c4dae9b4c5e47653d98fa2b8294954&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    description = data['overview']  # Fetch movie description
    return full_path, description

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, description = fetch_poster_and_description(movie_id)  # Fetch both poster and description
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_descriptions.append(description)
    
    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions

# Load the movies and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies)

# Streamlit UI
st.header('Movie Recommendation System')

# Movie select box
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend(selected_movie)

    # Create 5 columns for the recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display movie details (title, poster, and description) in each column
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.write(f"*Description:* {recommended_movie_descriptions[0]}")

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.write(f"*Description:* {recommended_movie_descriptions[1]}")

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.write(f"*Description:* {recommended_movie_descriptions[2]}")

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.write(f"*Description:* {recommended_movie_descriptions[3]}")

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.write(f"*Description:* {recommended_movie_descriptions[4]}")
    