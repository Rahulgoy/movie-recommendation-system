import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from tmdbv3api import TMDb

tmdb = TMDb()
tmdb.api_key = '58b44718dbd9cf348ac7a54c9320ae74'

from tmdbv3api import Movie

data = pd.read_csv("movie_data.csv")
st.title("Movie Recommendation System")
selected_movie_name = st.selectbox("Enter the movie:",data["movie_title"].values)


def create_sim():
    data = pd.read_csv('movie_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim


def recommend(m):
    m = m.lower()
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie your searched is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(sim[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
          
        lst = lst[1:20]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        unique_lst = []
        for x in l:
            if x not in unique_lst:
                unique_lst.append(x)
        unique_lst = unique_lst[:11] 
        return unique_lst

def get_posters(r):
    poster = []
    movie_title_list = []
    tmdb_movie = Movie()
    for movie_title in r:
        list_result = tmdb_movie.search(movie_title)
        movie_id = list_result[0].id
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
        data_json = response.json()
        poster.append('https://image.tmdb.org/t/p/original{}'.format(data_json['poster_path']))
    # movie_cards = {poster[i]: r[i] for i in range(len(r))}
    return (poster)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    posters = get_posters(recommendations)
    col1,col2,col3,col4,col5 = st.columns(5)
    col6,col7,col8,col9,col10 = st.columns(5)
    columns = [col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]

    for i in range(len(columns)):
        with columns[i]:
            st.text(recommendations[i])
            st.image(posters[i])
    