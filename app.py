import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from tmdbv3api import TMDb
import bs4 as bs
import urllib.request
import numpy as np

tmdb = TMDb()
tmdb.api_key = '58b44718dbd9cf348ac7a54c9320ae74'

from tmdbv3api import Movie

data = pd.read_csv("movie_data.csv")
st.title("Movie Recommendation System")
selected_movie_name = st.selectbox("Enter the movie:(Release till 2016)",data["movie_title"].values)


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

def ListOfGenres(genre_json):
    if genre_json:
        genres = []
        genre_str = ", " 
        for i in range(0,len(genre_json)):
            genres.append(genre_json[i]['name'])
        return genre_str.join(genres)


def date_convert(s):
    MONTHS = ['January', 'February', 'Match', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December']
    y = s[:4]
    m = int(s[5:-3])
    d = s[8:]
    month_name = MONTHS[m-1]

    result= month_name + ' ' + d + ' '  + y
    return result

def MinsToHours(duration):
    if duration%60==0:
        return "{:.0f} hours".format(duration/60)
    else:
        return "{:.0f} hours {} minutes".format(duration/60,duration%60)

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

    try:
        tmdb_movie = Movie()
        result = tmdb_movie.search(selected_movie_name)
        # get movie id and movie title
        movie_id = result[0].id
        movie_name = result[0].title
        
        # making API call
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
        data_json = response.json()
        imdb_id = data_json['imdb_id']
        poster = data_json['poster_path']
        img_path = 'https://image.tmdb.org/t/p/original{}'.format(poster)

        # getting list of genres form json
        genre = ListOfGenres(data_json['genres'])
        # getting votes with comma as thousands separators
        vote_count = "{:,}".format(result[0].vote_count)
        
        # convert date to readable format (eg. 10-06-2019 to June 10 2019)
        rd = date_convert(result[0].release_date)

        # convert minutes to hours minutes (eg. 148 minutes to 2 hours 28 mins)
        runtime = MinsToHours(data_json['runtime'])

        col11,col12 = st.columns(2)
        with col11:
            st.image(img_path)
        with col12:
            st.subheader("TITLE: "+ selected_movie_name.upper())
            st.write(result[0].overview)
            st.write(result[0].vote_average ,"("+vote_count+"votes)")
            st.write(genre)
            st.write("Release Date: "+ rd)
            st.write("Runtime: "+runtime)

    except:
        pass
    st.header("Recommendations")
    col1,col2,col3,col4,col5 = st.columns(5)
    col6,col7,col8,col9,col10 = st.columns(5)
    columns = [col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]
    for i in range(len(columns)):
        with columns[i]:
            st.text(recommendations[i].upper())
            st.image(posters[i])
    