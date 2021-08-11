from config import *

"""
Python file with the functions needed to save the data in raster format from the results for the main python program: 
"SumUpstream_Main". 
"""

def SaveRaster(array, output_path,  GT, Proj):
    """
    Function saves an array to a .tif raster file format. The nodata values should be -9999.
    :param array: array with results to save to a .tif raster file
    :param output_path: path and file name with which to save the .tif raster file
    :param GT: GEOTransform data
    :param Proj: raster projection
    :return: ----
    """
    #Step 1: Get drivers in order to save outputs as raster .tif files
    driver = gdal.GetDriverByName("GTiff")  # Get Driver and save it to variable
    driver.Register()  # Register driver variable

    # #Step 2: Create the raster files to save, with all the data: folder + name, number of columns (x),
    # number of rows (y), No. of bands, output data type (gdal type)
    outrs = driver.Create(output_path, xsize=array.shape[1], ysize=array.shape[0], bands=1, eType=gdal.GDT_Float32)

    #Step 3: Assign raster data and assaign the array to the raster
    outrs.SetGeoTransform(GT)  # assign geo transform data from the original input raster (same size)
    outrs.SetProjection(Proj)  # assign projection to raster from original input raster (same projection)
    outband = outrs.GetRasterBand(1)  # Create a band in which to input our array into
    outband.WriteArray(array)  # Read array into band
    # outband.SetNoDataValue(np.nan)  # Set no data value as Numpy nan
    outband.SetNoDataValue(-9999.0)  # Set no data value as Numpy nan
    outband.ComputeStatistics(0) #Set the raster statistics to the output raster

    #Step 4: Save raster to folder
    outband.FlushCache()
    outband = None
    outrs = None

    print("Saved raster: ", os.path.basename(output_path))