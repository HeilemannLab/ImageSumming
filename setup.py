"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.
"""

import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="ImageSumming",
                 version="220306",
                 author="Johanna Rahm",
                 author_email="johanna-rahm@gmx.de",
                 description="sum random patches of localizations, workflow addon for DeepSTORM2D",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 licence="GNU GENERAL PUBLIC LICENSE",
                 url="https:/github.com/JohannaRahm/ImageSumming",
                 packages=setuptools.find_packages(),
                 install_requires=["numpy",
                                   "matplotlib",
                                   "seaborn",
                                   "tqdm",
                                   "ipywidgets",
                                   "IPython",
                                   "pandas",
                                   "tifffile",
                                   "scikit-image",
                                   "pywin32",
                                   "plotly",
                                   "h5py"],
                   classifiers=["Programming Language :: Python :: 3",
                                  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                                  "Operating System :: OS Independent",],)
