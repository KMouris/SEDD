import numpy as np
import pandas as pd
import gdal
import os


"""
Python file with the functions needed to read the data from the input files for the main python program: 
"SumUpstream_Main". 
"""

def GetExtension(path):
    """
    Function gets file name and extracts the extension
    :param path: file path
    :return: the file extension
    """
    ext = os.path.splitext(path)[1]

    return ext

def GetASCII_Info(file_path):
    """
    Function extracts the information from the ASCII file in order to save the ASCII file header (to later save the file
    as an ASCII file) and extract the information needed to create a GEOTransform file (to later save the raster as a
    .tif file). The GEOTransform file has the following order: [Top left corner X, cell size, 0,Top left corner Y, 0,
     -cell size]

    :param file_path: path where a .txt ASCII raster file is located
    :return: the GEOtransform raster information and the ASCII file header (to later save the results)
    """
    # Save the ASCII raster information into a pandas data frame. It will have the following order:
    # ncols, nrows, xllcorner, yllcorner, cellsize, nodata_value
    # IF DELIMITER AND DECIMAL SEPARATOR ARE NOT A SPACE AND A COMMA (respectively) CHANGE THE FOLLOWING LINE
    df_head = pd.read_csv(file_path, delimiter='\s+', header=None, nrows=6, decimal=",")
    # print("Header:\n", df_head)

    # Save info as an array to save the data as GEOtransform type
    info_array = np.array(df_head.iloc[:, 1])
    # print(info_array)

    # Save needed information to create a GEOtransform variable (Top left corner X, cell size, 0,Top left corner Y, 0, -cell size)
    cell_size = float(info_array[4])  # Get cell size from the header information)
    ulx = float(info_array[2])  # Get Xmin (or ulx/llx) directly from the header information
    uly = float(info_array[3] + cell_size * info_array[1])  # Get uly by adding all the rows above the lly from the
    #                                                       # header information
    no_data = float(info_array[5])

    GT_array = [ulx, cell_size, 0.0, uly, 0.0, -cell_size]
    # print("GT: ", GT_array)
    GT = tuple(GT_array)  # Convert to type tuple to be read by save raster functions

    return GT, df_head, no_data

def GetArray_ASCII(file_path):
    """
    Function extracts the data from the ASCII .txt file (excluding the header)
    :param file_path: path where a .txt ASCII raster file is located
    :return: array with the raster data (including no data values)
    """
    array = np.array(pd.read_csv(file_path, delimiter='\s+', header=None, skiprows=6, decimal=","))
    # print("First value: ", array[1][660])

    return array

def GetRasterData(raster_path, data_info):
    """
    Function gets GEOTransform (gt) and projection data from a .tif raster file
    :param raster_path:  path where a .tif or other raster file format is located
    :param data_info: a boolean variable that is true if all information is needed, or false if only the projection is needed
    :return: gt (GEOTransform) and projection
    """
    raster = gdal.Open(raster_path) #Extract raster from path
    gt = raster.GetGeoTransform()  #Get Geotransform Data: Coordinate left upper corner, cellsize, 0, Coord. Lower right corner, 0, cell size
    proj = raster.GetProjection()  #Get projection of raster

    band = raster.GetRasterBand(1)  # Get raster band (the 1st one, since the inputs have only 1)
    no_data = np.float32(band.GetNoDataValue())  # Get NoData value

    if data_info:
        return gt, proj, no_data  #Return both variables
    else:
        return proj