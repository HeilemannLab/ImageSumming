"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handle widgets of DeepSTORM2DAddOns Jupyter Notebook.
"""


import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
from ipywidgets import widgets
from IPython.display import clear_output
import tkinter.filedialog as fd


class DefineFiles():
    def __init__(self, description, title, filetype, idx):
        """
        Define *.hdf5 files for analysis as center or neighbor, give short name to file.
        :param description: Short description of target file.
        :param title: Title of opened filedialog.
        :param filetype: File ending.
        :param idx: Idx of file.
        """
        self.got_file_name = False
        self.title = title  # title of browser window
        self.filetype = filetype  # filetype to filter in browser window
        self.file_text_box = self.create_file_box(description, idx)
        self.file_button = self.create_file_button()

    def create_file_button(self):
        button = widgets.Button(
            description="browse",
            disabled=False,
            button_style="",
            tooltip="browse for file")
        return button

    def open_file(self, b):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.lift()
        root.update()
        root.name = askopenfilename(title=self.title, filetypes=(self.filetype, ("all files", "*.*")))
        self.file_path = root.name
        root.update()
        root.destroy()
        self.file_text_box.value = self.file_path
        if os.path.isfile(self.file_path):
            self.got_file_name = True

    def create_file_box(self, type, idx):
        desc = "Path to " + type + " " + str(idx)
        style = {"description_width": "initial"}
        text = widgets.Text(value=str(""), placeholder="Insert path", description=str(desc), disabled=False,
                            style=style)
        return text

    def change_file_path_box(self, change):
        self.file_path = self.file_text_box.value
        if os.path.isfile(self.file_path):
            self.got_file_name = True


class RunAnalysis():
    def __init__(self, desc, tooltip):
        self.run_button = self.create_run_button(desc, tooltip)

    def create_run_button(self, desc, tooltip):
        button = widgets.Button(
            description=desc,
            disabled=False,
            button_style="",
            tooltip=tooltip)
        return button

    def create_clear_output(self):
        clear_output()


class SaveResults():
    def __init__(self):
        self.dir_name = ""
        self.got_dir = False
        self.save_button = self.create_save_button()
        self.box_filename = self.create_box_filename()
        self.dir_button = self.create_dir_button()
        self.dir_box = self.create_dir_box()

    def create_box_filename(self, val="", desc="Filename"):
        style = {"description_width": "initial"}
        text = widgets.Text(value=str(val), placeholder="name of folder", description=str(desc),
                            disabled=False, style=style)
        return text

    def create_dir_box(self, val="", desc="Directory", placeholder="Directory to save"):
        style = {"description_width": "initial"}
        text = widgets.Text(value=str(val), placeholder=placeholder, description=str(desc), disabled=False, style=style)
        return text

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

    def change_dir_box(self, change):
        self.dir_name = self.dir_box.value
        self.got_dir = True

    def create_save_button(self):
        button = widgets.Button(
            description="save",
            disabled=False,
            button_style="",
            tooltip="save the results")
        return button

    def create_clear_output(self):
        clear_output()


class ParameterBox():
    def __init__(self, desc, placeholder):
        self.value_box = self.create_value_box(desc, placeholder)

    def create_value_box(self, desc, placeholder):
        desc = desc
        style = {"description_width": "initial"}
        widget = widgets.Text(value=str(""), placeholder=placeholder, description=str(desc),
                              disabled=False, style=style)
        return widget
