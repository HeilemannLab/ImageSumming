"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

DeepSTORM2DAddOns:
- Convert Picasso csv file to DeepSTORM2D csv format.
- Split tif movie & corresponding localization file at defined frame.
"""


import numpy as np
import pandas as pd


class Converter():
    # Convert csv localization files from Picasso to DeepSTORM2D format
    def __init__(self):
        self.converted_file = []

    def convert(self, file_path):
        """
        Convert Picasso localization file into DeepSTORM2D format.
        frame idx starts at 1
        header = ,frame,x [nm],y [nm],Photon #,Sigma [nm]
        """
        file = pd.read_csv(file_path)
        file.index += 1
        file.frame += 1.0
        file = file[["frame", "x [nm]", "y [nm]", "intensity [photon]", "sigma [nm]"]]
        file.columns = ["frame", "x [nm]", "y [nm]", "Photon #", "Sigma [nm]"]
        self.converted_file = file


class ConverterH5():
    # Convert hdf5 localization files from Picasso to DeepSTORM2D format
    def __init__(self):
        self.converted_file = []

    def convert(self, file_path):
        """
        Convert Picasso localization file into DeepSTORM2D format.
        frame idx starts at 1
        header = ,frame,x [nm],y [nm],Photon #,Sigma [nm]
        """
        h5_file = pd.HDFStore(file_path, "r")
        file = h5_file.get("locs")
        file.index += 1
        file.frame += 1.0
        sigmas = file.loc[:, ["sx", "sy"]]
        file["Sigma [nm]"] = sigmas.mean(axis=1)
        file = file[["frame", "x", "y", "photons", "Sigma [nm]"]]
        file.columns = ["frame", "x [nm]", "y [nm]", "Photon #", "Sigma [nm]"]
        self.converted_file = file


class Splitter():
    # Split movie & localization file
    def __init__(self):
        self.split_movies = []
        self.split_locs = []

    def split(self, movie, loc_file, frame_idx):
        deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
        picasso_header = ['frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]',
                          'bkgstd [photon]', 'uncertainty_xy [nm]']

        if list(loc_file.columns) == picasso_header:
            # split loc file
            for i, row in loc_file.iterrows():
                if int(row["frame"]) == frame_idx:
                    split_idx = i
                    break
            self.split_locs = [loc_file[:split_idx], loc_file[split_idx:]]
            self.split_locs[1].frame -= frame_idx
            # split movie
            self.split_movies = [movie[:frame_idx], movie[frame_idx:]]
            print("Successfully split data.")
        elif list(loc_file.columns) == deep_storm_header:
            # split loc file
            for i, row in loc_file.iterrows():
                if int(row["frame"]) == frame_idx+1:
                    split_idx = i-1
                    break
            self.split_locs = [loc_file[:split_idx], loc_file[split_idx:]]
            self.split_locs[1].frame -= frame_idx
            # split movie
            self.split_movies = [movie[:frame_idx], movie[frame_idx:]]
            print("Successfully split data.")
        else:
            print("Wrong file type.")


class Merger():
    # Merge multiple movies & localization files
    def __init__(self):
        self.merged_movies = []
        self.merged_locs = []

    def merge(self, movies, loc_files):
        # merge movies
        merged_movies = movies[0]
        for c, movie in enumerate(movies):
            if c > 0:
                merged_movies = np.concatenate((merged_movies, movies[c]), axis=0)
        self.merged_movies = merged_movies
        # merge loc files
        frame_numbers = list(np.cumsum([max(file["frame"]) for file in loc_files]))
        frame_numbers.insert(0, 0)
        for file, frame_number in zip(loc_files, frame_numbers):
            file["frame"] = file["frame"] + frame_number
        self.merged_locs = pd.concat(loc_files, ignore_index=True)
        print("Successfully merged data.")


class SingleSplitter():
    # Split movie & localization file into single frames
    def __init__(self):
        self.single_frame_locs = []
        self.single_frame_movies = []

    def split(self, movie, loc_file):
        self.single_frame_locs = []
        for frame in loc_file["frame"].unique():
            single_frame_loc = loc_file[loc_file["frame"] == frame]
            self.single_frame_locs.append(single_frame_loc)

        self.single_frame_movies = []
        for i in range(len(movie)):
            new_movie = movie[i:i+1]
            self.single_frame_movies.append(new_movie)

        print("Successfully split data.")
