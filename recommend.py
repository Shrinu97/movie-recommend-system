from typing import Dict

import streamlit as st
import pickle
import pandas as pd
import requests

# we dumped the data from google-colab to pycharm using pickle library
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# we create a dataframe of sorted data of google-colab coding.
movies = pd.DataFrame(movie_dict)

# we dumped data sorted using similarity function
similarity = pickle.load(open('similarity.pkl', 'rb'))


# we failed to linked google-colab coding and pycharm , we create a dataframe
# same thing we have to do for the recommend function.


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?language=en-US'.format(movie_id)
    headers = dict(
        Authorization='Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYjA5ZDI4MmJhMzlmZDQ2ZmFhYTA4NmY4ZTA5MTE2YSIsInN1YiI6IjY0ZDFlNzczNTQ5ZGRhMDExYzI5NzM4MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.gjDJRgcp9MQBqz_TsdoZYZ6id1sa111ouo_UK2GgWIs'
        , accept='application/json')

    response = requests.request("GET", url, headers=headers, data={})

    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)

        # this will fetch poster of recommended movies from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.title('Movie recommender system')

choice = st.selectbox("Pick one movie", movies['title'].values)
if st.button("Recommend"):
    names, posters = recommend(choice)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


