"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle saving of DeepSTORM2DAddOns Jupyter Notebook.
"""


import os
import csv
import tifffile


def save_convert_file(data_path, converted_file):
    # Convert localization file
    save_dir = os.path.splitext(data_path)[0] + "_conv.csv"
    converted_file.to_csv(save_dir)
    print("File successfully saved at " + save_dir)


def save_split_files(movie_path, loc_path, split_movies, split_locs, frame_idx):
    # Split movie & localization file
    save_dirs_locs = [os.path.splitext(loc_path)[0] + "_A.csv",
                 os.path.splitext(loc_path)[0] + "_B.csv"]
    save_dirs_movies = [os.path.splitext(movie_path)[0] + "_A.tif",
                 os.path.splitext(movie_path)[0] + "_B.tif"]

    deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
    picasso_header = ['frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]',
                      'bkgstd [photon]', 'uncertainty_xy [nm]']
    picasso_header_str = ['"frame"', '"x [nm]"', '"y [nm]"', '"sigma [nm]"', '"intensity [photon]"',
                          '"offset [photon]"', '"bkgstd [photon]"', '"uncertainty_xy [nm]"']

    if list(split_locs[0].columns) == deep_storm_header:
        header = deep_storm_header
        for file in split_locs:
            file.index = [*range(1, len(file)+1)]
    elif list(split_locs[0].columns) == picasso_header:
        header = picasso_header_str
        for file in split_locs:
            file.index = [*range(len(file))]
            file.index.name = '"id"'

    for file, save_path in zip(split_locs, save_dirs_locs):
        file.to_csv(save_path, header=header, quoting=csv.QUOTE_NONE)
        print("File saved at " + save_path)
    for file, save_path in zip(split_movies, save_dirs_movies):
        file = file.astype("int16")
        tifffile.imwrite(save_path, file)
        print("File saved at " + save_path)


def save_merge_files(dir_path, file_name, merged_movies, merged_locs):
    # Merge multiple movies & localization files
    deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
    picasso_header = ['frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]',
                      'bkgstd [photon]', 'uncertainty_xy [nm]']
    picasso_header_str = ['"frame"', '"x [nm]"', '"y [nm]"', '"sigma [nm]"', '"intensity [photon]"',
                          '"offset [photon]"', '"bkgstd [photon]"', '"uncertainty_xy [nm]"']

    if list(merged_locs) == deep_storm_header:
        header = deep_storm_header
        merged_locs.index = [*range(1, len(merged_locs)+1)]
    elif list(merged_locs) == picasso_header:
        header = picasso_header_str
        merged_locs.index = [*range(len(merged_locs))]
        merged_locs.index.name = '"id"'

    merged_locs.to_csv(dir_path + "\\" + file_name + ".csv", header=header, quoting=csv.QUOTE_NONE)
    merged_movies = merged_movies.astype("int16")
    tifffile.imwrite(dir_path + "\\" + file_name + ".tif", merged_movies)
    print("Files successfully saved at " + dir_path)


def save_single_split_files(dir_path, filename, movies, locs):
    save_path = dir_path + "\\" + filename

    deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
    picasso_header = ['frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]',
                      'bkgstd [photon]', 'uncertainty_xy [nm]']
    picasso_header_str = ['"frame"', '"x [nm]"', '"y [nm]"', '"sigma [nm]"', '"intensity [photon]"',
                          '"offset [photon]"', '"bkgstd [photon]"', '"uncertainty_xy [nm]"']

    if list(locs[0].columns) == deep_storm_header:
        for c, (movie, loc) in enumerate(zip(movies, locs), 1):
            loc.to_csv(save_path + "_" + str(c) + ".csv", header=deep_storm_header, quoting=csv.QUOTE_NONE)
            movie = movie.astype("int16")
            tifffile.imwrite(save_path + "_" + str(c) + ".tif", movie)
    elif list(locs[0].columns) == picasso_header:
        for c, (movie, loc) in enumerate(zip(movies, locs), 1):
            loc.index.name = '"id"'
            loc.to_csv(save_path + "_" + str(c) + ".csv", header=picasso_header_str, quoting=csv.QUOTE_NONE)
            movie = movie.astype("int16")
            tifffile.imwrite(save_path + "_" + str(c) + ".tif", movie)

    print("Files saved at " + save_path)
