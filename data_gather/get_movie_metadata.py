import numpy as np
import pandas as pd 
import json
import requests


# ------------------------------------------------------------------ #
# Gather the data from the movie_metadata.csv file. This was
# downloaded from Kaggle 
# https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset
# We will use this movie list to gather synopses and genres for each 
# movie, from the OMDB API, in this data set.
# ------------------------------------------------------------------ #

OMDB_API_URL = "http://www.omdbapi.com/?i={}&plot=full&r=json"

movie_data = pd.read_csv('../data/movie_metadata.csv')


synopses = []
for i in range(len(movie_data)):
    movie = movie_data['movie_title'][i].rstrip()
    ## use the IMDB ID to search
    imdb_id = movie_data['movie_imdb_link'][i].split('/')[4]
    r = requests.get(OMDB_API_URL.format(imdb_id))
    mdata = r.json()
    d = {
        'plot': mdata['Plot'],
        'title': mdata['Title'],
        'genres': mdata['Genre']
    }
    synopses.append(d)


data = {
    'data': synopses,
    'length': len(synopses)
}


with open('../data/movie_metadata.json', 'w') as fp:
    json.dump(data, fp)
