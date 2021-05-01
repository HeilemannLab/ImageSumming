"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Save localizations of single frames found by DeepSTORM2D to one csv file. Filter out localizations below a
confidence threshold.
"""


import os


def save(dir_path, threshold, locs):
    for file in os.listdir(dir_path):
        if file.endswith(".csv") and "_avg" in file and "filtered" not in file:
            save_path = os.path.join(dir_path, file[:-4] + "_filtered.csv")
    filtered_locs = locs[locs["confidence [a.u]"] >= threshold]
    filtered_locs.to_csv(save_path, index=False)
    print("Filtered localizations are saved!")
