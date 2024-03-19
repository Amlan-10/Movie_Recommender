import streamlit as st
import pickle
import numpy as np
import requests

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={movie_title}"
    data = requests.get(url)
    data = data.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None

def recommend(movie):
    movie_index = np.where(movie_titles == movie)[0][0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in similar_movies:
        recommended_movie_title = movie_titles[i[0]]
        poster_url = fetch_poster(recommended_movie_title)
        if poster_url:
            recommended_movies.append((recommended_movie_title, poster_url))
        else:
            recommended_movies.append((recommended_movie_title, None))
    return recommended_movies

movies_df = pickle.load(open('movies.pkl', 'rb'))
movie_titles = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movie_titles)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write("Recommended movies:")
    col1, col2, col3, col4, col5 = st.columns(5)
    for movie, poster_url in recommendations:
        if poster_url:
            with col1:
                st.write(movie)
                st.image(poster_url, caption=movie, use_column_width=True, width=150)
