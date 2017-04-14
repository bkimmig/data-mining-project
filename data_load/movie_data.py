import numpy as np 
import json
import matplotlib.pyplot as plt

def remove_items(data, frequency_threshold=0.05):
    """
    Remove the items that occur less that the frequency specified 
    amount of the time.
    
    Parameters
    ----------
    data: list
        list of genres
    frequency_threshold: float
    
    Returns
    -------
    data: list
    """
    
    unique_items, counts = np.unique(np.concatenate(data), return_counts=True)
    freq= counts/np.sum(counts)
    keep_items = set(unique_items[freq > frequency_threshold])
    
    items = []
    for i in range(len(data)):
        items.append(list(set(data[i]) & keep_items))
    return items


def one_hot(data):
    """
    Make a one-hot encoding of the genre data. Every
    movie should have a list of genres.
    
    Parameters
    ----------
    data: list
        a list of lists.
        
    Returns
    -------
    labels: np.array
        the labels associated with the list shape (len(unique_genres), )
    one_hot: np.array
        the one hot encoding, with shape (len(data), len(unique_genres))
    
    """
    labels = np.unique(np.concatenate(data))
    one_hot = np.zeros((len(data), len(labels)), dtype=bool)
    for i in range(len(data)):
        for j in range(len(data[i])):
            one_hot[i] += data[i][j] == labels
    return labels, one_hot.astype(int)


class MovieData(object):

	DATAPATH = '../data/movie_metadata.json'
	def __init__(self, min_genre_frequency=0.1, verbose=False):
		self.min_genre_frequency = min_genre_frequency
		self.verbose = verbose
		self._open_data()
		self._unpack_genres()

	def _open_data(self):
		with open(self.DATAPATH, 'r') as f:
		    movie_data = json.load(f)

		plots = []
		genres = []
		for movie in movie_data['data']:
		    plots.append(movie['plot'])
		    genres.append([genres.strip() 
		    			   for genres in movie['genres'].split(',')])

		self.plots = plots
		self._genres = genres

	def _unpack_genres(self):

		self._genres_unique, self._genres_count = np.unique(
			np.concatenate(self._genres),
			return_counts=True
		)
		self._genre_frequency = self._genres_count/len(self.plots)

		self.genres = remove_items(self._genres, self.min_genre_frequency)
		self.genres_unique, self.genres_count = np.unique(
			np.concatenate(self.genres),
			return_counts=True
		)
		self.genre_frequency = self.genres_count/len(self.plots)#/np.sum(self.genres_count)
		self.genre_labels, self.one_hot_genres = one_hot(self.genres)

		if self.verbose:
			print('Genres occuring more than {}% of the time'.format(
				self.min_genre_frequency)
			)
			for genre in self.genres_unique[genre_mask]:
				print(genre)
		return

	def latex_print_genres(self):
		self.genres_unique
		self.genre_frequency
		print("N movie genres : {}".format(len(self.genre_frequency)))

		for i in range(len(self.genre_frequency)):
		    print(r"{} & {:.3f}\% \\".format(
		        self.genres_unique[i], 
		        self.genre_frequency[i]*100)
		    )
		return


	def plot_genres(self, savefig=False):
		idx = np.arange(len(self._genre_frequency))
		space = 0.1

		fig = plt.figure('')
		ax = fig.add_subplot(111)
		ax.bar(idx, self._genre_frequency*100)
		ax.set_xticks(idx)
		ax.set_xticklabels(self._genres_unique, rotation='vertical')

		ax.hlines(
			self.min_genre_frequency*100, 
			-5, 
			np.max(idx)+5, 
			colors='r', 
			linestyles='dashed'
		)
		ax.set_xlim((-1, np.max(idx)+1))

		ax.set_ylabel('Percent Occurance')
		ax.set_xlabel('Genre')

		plt.tight_layout()
		if savefig:	
			plt.savefig(savefig)
		plt.show()

	def plot_one_hot_genres(self, savefig=False):
		idx = np.arange(len(self.genre_frequency))
		space = 0.1

		fig = plt.figure('')
		ax = fig.add_subplot(111)
		ax.imshow(self.one_hot_genres, aspect='auto')
		ax.set_xticks(idx)
		ax.set_xticklabels(self.genre_labels, rotation='vertical')

		ax.set_ylabel('Movie Index')
		ax.set_xlabel('Genre')
		plt.tight_layout()
		if savefig:	
			plt.savefig(savefig)
		plt.show()

