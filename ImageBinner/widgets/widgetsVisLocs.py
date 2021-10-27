"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle widgets of VisualizeDeepSTORM2DLocs Jupyter Notebook.
"""

import tkinter as tk
import os
from ipywidgets import widgets
import tkinter.filedialog as fd
from IPython.display import clear_output


class DefineDirectory():
    def __init__(self, description, value=""):
        """
        Define *.hdf5 files for analysis as center or neighbor, give short name to file.
        :param description: Short description of target file.
        :param title: Title of opened filedialog.
        :param filetype: File ending.
        :param idx: Idx of file.
        """
        self.got_dir = False
        self.dir_name = ""
        self.dir_box = self.create_dir_box(description, value)
        self.dir_button = self.create_dir_button()

    def create_dir_button(self):
        button = widgets.Button(
            description="browse",
            disabled=False,
            button_style="",
            tooltip="browse for directory")
        return button

    def open_dir(self, b):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.lift()
        root.update()
        root.name = fd.askdirectory(initialdir=os.getcwd(), title="Please select a directory")
        root.update()
        root.destroy()
        self.dir_name = root.name
        self.dir_box.value = self.dir_name
        self.got_dir = True

    def create_dir_box(self, description, val=""):
        style = {"description_width": "initial"}
        text = widgets.Text(value=str(val), placeholder="directory to be searched in", description=str(description),
                            disabled=False, style=style)
        return text

    def change_dir_box(self, change):
        self.dir_name = self.dir_box.value
        self.got_dir = True


class Parameters():
    def __init__(self, pixel_size,  confidence_threshold):
        self.pixel_size = self.create_pixel_size_box(pixel_size)
        self.confidence_threshold = self.create_confidence_threshold_box(confidence_threshold)

    def create_pixel_size_box(self, val):
        desc = "Pixel size [nm]"
        style = {"description_width": "initial"}
        widget = widgets.Text(value=str(val), placeholder="Insert pixel size", description=str(desc), disabled=False, style=style)
        return widget

    def create_confidence_threshold_box(self, val):
        desc = "Confidence threshold"
        style = {"description_width": "initial"}
        widget = widgets.Text(value=str(val), placeholder="locs below are filtered out", description=str(desc), disabled=False, style=style)
        return widget


class RunAnalysis():
    def __init__(self):
        self.run_load_button = self.create_run_load_button()

    def create_run_load_button(self):
        button = widgets.Button(
            description="load & display",
            disabled=False,
            button_style="",
            tooltip="display input data")
        return button

    def create_clear_output(self):
        clear_output()


class SaveResults():
    def __init__(self):
        self.save_button = self.create_save_button()

    def create_save_button(self):
        button = widgets.Button(
            description="save",
            disabled=False,
            button_style="",
            tooltip="save the results")
        return button

    def create_clear_output(self):
        clear_output()
