import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    #print(similarity[index[0]])
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    link_movie=[]
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        link_movie.append(movies.iloc[i[0]].homepage)

    return recommended_movie_names,recommended_movie_posters,link_movie


st.header('Movie Recommender System')
movies = pickle.load(open('prjmcl\\artifacts\\movie_list.pkl','rb'))
similarity = pickle.load(open('prjmcl\\artifacts\\similarity.pkl','rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown",options=movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters,link_movie = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.link_button(url=link_movie[0],label="Watch")
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.link_button(url=link_movie[1],label="Watch")

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.link_button(url=link_movie[2],label="Watch")
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.link_button(url=link_movie[3],label="Watch")
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.link_button(url=link_movie[4],label="Watch")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        for i in range(5):
            st.text(movie_list[i])
            st.image(fetch_poster(movies["movie_id"][i]))
            st.link_button(url=movies["homepage"][i],label="Watch")
    with col2:
        for i in range(5,10):
            st.text(movie_list[i])
            st.image(fetch_poster(movies["movie_id"][i]))
            st.link_button(url=movies["homepage"][i],label="Watch")
    with col3:
        for i in range(10,15):
            st.text(movie_list[i])
            st.image(fetch_poster(movies["movie_id"][i]))
            st.link_button(url=movies["homepage"][i],label="Watch")
    with col4:
        for i in range(50,55):
            st.text(movie_list[i])
            st.image(fetch_poster(movies["movie_id"][i]))
            st.link_button(url=movies["homepage"][i],label="Watch")
    with col5:
        for i in range(100,105):
            st.text(movie_list[i])
            st.image(fetch_poster(movies["movie_id"][i]))
            st.link_button(url=movies["homepage"][i],label="Watch")
