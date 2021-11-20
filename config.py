"""File contains all needed modules and libraries, as well as the user input. """

# import all needed basic python libraries
try:
    import glob
    import os
    import sys
    import time
except ModuleNotFoundError as b:
    print('ModuleNotFoundError: Missing basic libraries (required: glob, os, sys, time')
    print(b)

# import additional python libraries
try:
    import gdal
    import numpy as np
    import pandas as pd
except ModuleNotFoundError as b:
    print('ModuleNotFoundError: Missing fundamental packages (required: gdal, numpy, pandas')
    print(b)


"""
* Input rasters:
    *All rasters must have the same extent, pixel size (resolution) 
- flowdir_path: string, path for glow direction raster (in .txt ASCII file format or raster format)
- traveltime_path: string, path for travel time (per cell) raster (in .txt ASCII file format or raster format)
- proj_raster: string, path for the projection raster: in case both input rasters are in .txt format (program gets 
  the raster projection)
- results_path: string, path where to save the resulting total travel time raster (.tif)
"""

flowdir_path = r'C:\Users\Mouris\git\SEDD\Example_files\fl_dir_4000.txt'
traveltime_path = r'C:\Users\Mouris\git\SEDD\Example_files\traveltime_percell_corr.txt'
proj_raster = r'C:\Users\Mouris\git\SEDD\Example_files\fildembanja2.tif'
results_path = r'C:\Users\Mouris\git\SEDD\Results'
