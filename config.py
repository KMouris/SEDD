"""Loads required modules and libraries, and defines user input. """

# import all needed basic python libraries
try:
    import glob
    import os
    import sys
    import time
except ImportError as e:
    print('ModuleNotFoundError: Failed loading standard libraries (glob, os, sys, time)')
    print(e)

# import additional python libraries
try:
    import gdal
    import numpy as np
    import pandas as pd
except ImportError as e:
    print('ModuleNotFoundError: Missing fundamental packages (required: gdal, numpy, pandas)')
    print(e)

"""Input rasters:
    *All rasters must have the same extent, pixel size (resolution)
- flowdir_path: string, path for glow direction raster (in .txt ASCII file format or raster format)
- traveltime_path: string, path for travel time (per cell) raster (in .txt ASCII file format or raster format)
- proj_raster: string, path for the projection raster: in case both input rasters are in .txt format (program gets
  the raster projection)
- results_path: string, path where to save the resulting total travel time raster (.tif)
"""

base_dir = os.path.abspath("") + "/"
flowdir_path = r"" + base_dir + "example-files/fl_dir_4000.txt"
traveltime_path = r"" + base_dir + "example-files/traveltime_percell_corr.txt"
proj_raster = r"" + base_dir + "example-files/fildembanja2.tif"
results_path = r"" + base_dir + "results"
