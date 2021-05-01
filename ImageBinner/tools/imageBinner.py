"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

ImageBinner functionalities.
"""


import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm.notebook import tqdm


def get_dimensions(movies):
    """
    Get dimensions of movies (number frames, width, height)
    Code adapted from DeepSTORM2D ZeroCostDL4Mic Notebook
    """
    movies_dim = []
    for movie in movies:
        if len(movie.shape) == 3:
            (number_of_frames, M, N) = movie.shape
        elif len(movie.shape) == 2:
            (M, N) = movie.shape
            number_of_frames = 1
        movies_dim.append((number_of_frames, M, N))
    return movies_dim


def vis_input_density(movies_dim, movies_locs, pixel_size):
    """Density per frame in em/ym², boxplot per movie"""
    for idx in range(len(movies_locs)):
        area = (movies_dim[idx][1]*pixel_size/1000)*(movies_dim[idx][2]*pixel_size/1000)  # patch area in ym²
        density = []
        for frame_idx in movies_locs[idx]["frame"].unique():
            density.append(len(movies_locs[idx][movies_locs[idx]["frame"] == frame_idx])/area)
        fig = plt.figure(figsize=(3, 5))
        ax = sns.boxplot(data=density, color="cornflowerblue", showmeans=True,
                         meanprops={"marker": "*", "markerfacecolor": "white", "markeredgecolor": "0.25", "markersize": "10"})
        ax.set_title("Density per frame of movie " + str(idx+1))
        ax.set_ylabel("density [emitters/\u00B5m²]")
        ax.set(xlabel=None)
        plt.show()
        print("Mean density of movie " + str(idx+1) + ": {0:.3f} em/\u00B5m²".format(np.mean(density)))


def vis_patch_density(random_locs, pixel_size, patch_size):
    """Boxplot: Density per patch in em/ym²"""
    area = (patch_size*pixel_size/1000)**2  # patch area in ym²
    density = pd.DataFrame([len(i)/area for i in random_locs], columns=["patches"])
    fig = plt.figure(figsize=(3, 5))
    ax = sns.boxplot(data=density, color="cornflowerblue", showmeans=True,
                     meanprops={"marker": "*", "markerfacecolor": "white", "markeredgecolor": "0.25", "markersize": "10"})
    ax.set_title("Density per binned patch")
    ax.set_ylabel("density [emitters/\u00B5m²]")
    ax.set(xlabel=None)
    plt.show()
    print("Mean density: {0:.3f} em/\u00B5m²".format(density["patches"].mean()))


def xy_loc_vis(frame_locs, pixel_size):
    x = frame_locs["x [nm]"]/pixel_size
    y = frame_locs["y [nm]"]/pixel_size
    return x, y


class GetPatches():
    def __init__(self):
        self.random_patches = []
        self.random_patches_idx = []  # (movie, frame) idx per patch
        self.random_patch_nm = []  # start idx of patch window
        self.random_locs = []
        self.random_patches_binned = []
        self.random_patches_binned_idx = []  # lst of idx per binned patches
        self.random_locs_binned = []

    def clear(self):
        self.__init__()

    def get_patch_locs(self, n, m, patch_size, frame_locs, pixel_size):
        # valid idx of patches
        nm_idx = []
        for i in range(n, n + patch_size):
            for j in range(m, m + patch_size):
                nm_idx.append([j, i])
        x = frame_locs["x [nm]"].map(lambda x: int(np.floor(x / pixel_size)))
        y = frame_locs["y [nm]"].map(lambda y: int(np.floor(y / pixel_size)))
        # filter based on valid idx
        loc_idx = []
        for idx, (x_loc, y_loc) in enumerate(zip(x, y)):
            if [x_loc, y_loc] in nm_idx:
                loc_idx.append(idx)
        patch_locs = frame_locs.iloc[loc_idx]
        patch_locs.loc[:, "x [nm]"] = patch_locs["x [nm]"].apply(lambda x: x - (m * pixel_size))
        patch_locs.loc[:, "y [nm]"] = patch_locs["y [nm]"].apply(lambda x: x - (n * pixel_size))
        return patch_locs

    def get_random_patches(self, n_patches, movies, movies_locs, patch_size, min_number_of_emitters_per_patch, pixel_size):
        self.random_patches = np.asarray([np.zeros((patch_size, patch_size), dtype=int) for _ in range(n_patches)])
        self.random_locs = []
        c = 0
        with tqdm(total=n_patches, desc="Patches created") as pbar:
            while c < n_patches:
                # choose random movie
                random_movie = np.random.randint(0, len(movies))
                # choose random frame
                random_frame = np.random.randint(0, movies[random_movie].shape[0])
                # choose random patch
                try:
                    random_n = np.random.randint(0, movies[random_movie].shape[1] - patch_size + 1)
                    random_m = np.random.randint(0, movies[random_movie].shape[2] - patch_size + 1)
                except ValueError:
                    print("Error: Patch size has to be <= input shape.")
                    break
                # get patch
                patch_locs = self.get_patch_locs(random_n, random_m, patch_size, movies_locs[random_movie][
                    movies_locs[random_movie]["frame"] == random_frame], pixel_size)
                if len(patch_locs) >= min_number_of_emitters_per_patch:
                    self.random_patches_idx.append([random_movie+1, random_frame])
                    self.random_patches[c] = movies[random_movie][random_frame - 1][random_n:random_n + patch_size,
                                             random_m:random_m + patch_size]
                    self.random_locs.append(patch_locs)
                    self.random_patch_nm.append([random_n, random_m])
                    c += 1
                    pbar.update(1)

    def bin_patches(self, n_patches, bin_size, patch_size, camera_noise):
        self.random_patches_binned = np.asarray([np.zeros((patch_size, patch_size), dtype=int) for i in range(n_patches)])
        self.random_locs_binned = []
        with tqdm(total=n_patches, desc="Patches binned") as pbar:
            for patch_idx in range(n_patches):
                random_idx = random.sample(range(len(self.random_patches)), bin_size)
                self.random_patches_binned_idx.append(random_idx)
                chosen_patches = [self.random_patches[idx] for idx in random_idx]
                # add patches together
                binned_patches = np.full(np.shape(chosen_patches[0]), 0)
                for i in range(0, len(chosen_patches)):
                    binned_patches += chosen_patches[i]
                # correct for camera noise
                binned_patches -= np.full(np.shape(binned_patches[0]), camera_noise*(bin_size-1))
                self.random_patches_binned[patch_idx] = binned_patches
                chosen_locs = [self.random_locs[idx] for idx in random_idx]
                binned_locs = pd.concat(chosen_locs, ignore_index=True)
                self.random_locs_binned.append(binned_locs)
                pbar.update(1)

    def create_patches(self, n_patches, movies, loc_files, patch_size, n_binned_patches, bin_size, min_emitter,
                       pixel_size, camera_noise, augmentation=False):
        self.clear()
        self.get_random_patches(n_patches, movies, loc_files, patch_size, min_emitter, pixel_size)
        self.bin_patches(n_binned_patches, bin_size, patch_size, camera_noise)
