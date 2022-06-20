"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle data loading for DeepSTORM2DAddOns Jupyter Notebook.
"""

from skimage import io
import pandas as pd

# Split movie & localization file

class DataSplit():
    def __init__(self):
        self.movie = []  # tif movies
        self.loc_file = []  # localization csv file

    def load_movie(self, movie_dir):
        return io.imread(movie_dir)

    def load_localization(self, loc_dir):
        # for both deepstorm & picasso
        loc_file = pd.read_csv(loc_dir, index_col=0)
        return loc_file

    def load_data(self, movie_dir, loc_dir):
        self.movie = self.load_movie(movie_dir)
        self.loc_file = self.load_localization(loc_dir)


class DataMerge():
    def __init__(self):
        self.movies = []
        self.loc_files = []

    def load_movie(self, movie_dir):
        return io.imread(movie_dir)

    def load_localization(self, loc_dir):
        loc_file = pd.read_csv(loc_dir, index_col=0)
        return loc_file

    def load_data(self, movie_dirs, loc_dirs):
        self.movies = [self.load_movie(movie_dir) for movie_dir in movie_dirs]
        self.loc_files = [self.load_localization(loc_dir) for loc_dir in loc_dirs]


class SumFrames():
    def __init__(self):
        self.movie = []

    def load_movie(self, movie_dir):
        self.movie = io.imread(movie_dir)