# Data mining project

## Authors
- Brian Kimmig
- Jesus Zarate

# Gathering the Data

This is a list of the data files and sources, how we gather the data, and where the gathered data lives and what it contains.

## Movie Metadata (Kaggle)

We will get synopses for the movie data in the file from a <a href='https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset'> Kaggle Dataset </a>. If this is not enough data we will look for other sources. The data lives in the directory 
	
	$ data-mining-project/data

and the script that will gather the data lives in 

	$ data-mining-project/data_gather/get_movie_metadata.py

The script gathers all the data and puts it in a JSON file. I ignore all of the full data files and only put the zipped files in the repository to avoid taking up too much space.

The json file generated from this is
	
	$ data-mining-project/data/movie_metadata.json

This json file contains 3 parameters for every movie.

1. title - string
2. plot - string
3. genres - comma separated

### Data Errors - Movie Metadata

Star wars was not the movie but a documentary, I changed the IMDB ID to the movie to get the plot (from tt5289954 to tt2488496) 