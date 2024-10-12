
import streamlit as st
import pickle
import pandas as pd 
import requests

# Function to fetch movie details including poster, description, cast, and crew
def fetch_movie_details(movie_id):
    api_key = "41c4dae9b4c5e47653d98fa2b8294954"
    
    # Fetch movie details (poster, description, genres, rating, runtime, tagline)
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    movie_data = requests.get(movie_url).json()
    
    poster_path = movie_data['poster_path']
    full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    description = movie_data['overview']
    genres = ", ".join([genre['name'] for genre in movie_data['genres']])
    rating = movie_data['vote_average']
    runtime = movie_data['runtime']
    tagline = movie_data['tagline']
    
    # Fetch movie cast and crew
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US"
    credits_data = requests.get(credits_url).json()
    
    cast = [member['name'] for member in credits_data['cast'][:5]]  # Top 5 cast members
    crew = [member['name'] + " (" + member['job'] + ")" for member in credits_data['crew'] if member['job'] in ['Director', 'Producer']]
    
    return full_poster_path, description, genres, rating, runtime, tagline, cast, crew

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    recommended_movie_genres = []
    recommended_movie_ratings = []
    recommended_movie_runtimes = []
    recommended_movie_taglines = []
    recommended_movie_cast = []
    recommended_movie_crew = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        (poster, description, genres, rating, runtime, tagline, cast, crew) = fetch_movie_details(movie_id)
        
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_descriptions.append(description)
        recommended_movie_genres.append(genres)
        recommended_movie_ratings.append(rating)
        recommended_movie_runtimes.append(runtime)
        recommended_movie_taglines.append(tagline)
        recommended_movie_cast.append(cast)
        recommended_movie_crew.append(crew)
    
    return (recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions, 
            recommended_movie_genres, recommended_movie_ratings, recommended_movie_runtimes, 
            recommended_movie_taglines, recommended_movie_cast, recommended_movie_crew)

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
    (recommended_movie_names, 
     recommended_movie_posters, 
     recommended_movie_descriptions, 
     recommended_movie_genres, 
     recommended_movie_ratings, 
     recommended_movie_runtimes, 
     recommended_movie_taglines, 
     recommended_movie_cast, 
     recommended_movie_crew) = recommend(selected_movie)
    
    # Display recommendations in single column layout
    for i in range(5):
        st.subheader(recommended_movie_names[i])
        st.image(recommended_movie_posters[i])
        st.write(f"**Description:** {recommended_movie_descriptions[i]}")
        st.write(f"**Genres:** {recommended_movie_genres[i]}")
        st.write(f"**Rating:** {recommended_movie_ratings[i]}")
        st.write(f"**Runtime:** {recommended_movie_runtimes[i]} minutes")
        st.write(f"**Tagline:** {recommended_movie_taglines[i]}")
        st.write(f"**Cast:** {', '.join(recommended_movie_cast[i])}")
        st.write(f"**Crew:** {', '.join(recommended_movie_crew[i])}")
        st.markdown("---")
    