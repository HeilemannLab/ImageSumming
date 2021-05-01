"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle data loading of VisualizeDeepSTORM2DLocs Jupyter Notebook.
"""


import os
import pandas as pd
from skimage import io


class LoadFiles():
    def __init__(self):
        self.gt_tifs = []  # widefield images
        self.predicted_stack = []  # predicted images
        self.gt_locs = []  # gt localizations
        self.widefield_tif = []  # widefield image
        self.predicted_tifs = []  # predicted image
        self.predicted_locs = []  # predicted localizations

    def get_files(self, dir_path_predictions):
        gt_loc_path = []
        for file in os.listdir(dir_path_predictions):
            if file.endswith(".csv") and "_avg" not in file:
                gt_loc_path = os.path.join(dir_path_predictions, file)

        for file in os.listdir(dir_path_predictions):
            if file.endswith(".tif") and "Widefield" not in file and "Predicted" not in file:
                gt_tif_path = os.path.join(dir_path_predictions, file)

        for file in os.listdir(dir_path_predictions):
            if file.endswith(".tif") and "Widefield" in file:
                widefield_tif_path = os.path.join(dir_path_predictions, file)

        for file in os.listdir(dir_path_predictions):
            if file.endswith(".csv") and ("_avg" in file or "_max" in file):  #  or "_max" (from local av = False)
                predicted_loc_path = os.path.join(dir_path_predictions, file)

        for file in os.listdir(dir_path_predictions):
            if file.endswith(".tif") and "Predicted" in file and "stacked" not in file:
                predicted_tif_path = os.path.join(dir_path_predictions, file)

        for file in os.listdir(dir_path_predictions):
            if file.endswith(".tif") and "Predicted_stacked" in file:
                predicted_stack_tif_path = os.path.join(dir_path_predictions, file)

        # load files
        self.gt_tifs = io.imread(gt_tif_path)
        self.predicted_stack = io.imread(predicted_stack_tif_path)
        if gt_loc_path:
            self.gt_locs = pd.read_csv(gt_loc_path, index_col=0)
        self.widefield_tif = io.imread(widefield_tif_path)
        self.predicted_tif = io.imread(predicted_tif_path)
        self.predicted_locs = pd.read_csv(predicted_loc_path)
