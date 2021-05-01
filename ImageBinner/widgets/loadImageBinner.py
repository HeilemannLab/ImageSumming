"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle data loading of ImageBinner Jupyter Notebook.
"""


from skimage import io
import pandas as pd


class Data():
    def __init__(self):
        self.movies = []  # list of tif movies
        self.loc_files = []  # list of localization csv files

    def load_movies(self, movie_dirs):
        movies = [io.imread(i) for i in movie_dirs]
        return movies

    def load_localizations(self, loc_dirs):
        loc_files = [pd.read_csv(i, index_col=0) for i in loc_dirs]
        deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
        deep_storm_format = [True if list(i.columns) == deep_storm_header else False for i in loc_files]
        for i, ds_format in zip(loc_files, deep_storm_format):
            if not ds_format:
                i["frame"] += 1
        return loc_files

    def load_data(self, movie_dirs, loc_dirs):
        self.movies = self.load_movies(movie_dirs)
        self.loc_files = self.load_localizations(loc_dirs)
