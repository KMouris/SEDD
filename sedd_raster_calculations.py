"""
Module with functions to read, extract data and save raster functions for the sedd model calculations.
"""
from config import *


def get_ascii_info(file_path):
    """
    Function extracts the information from the ASCII file in order to save the ASCII file header (to later save the file
    as an ASCII file) and extract the information needed to create a GEOTransform file (to later save the raster as a
    .tif file). The GEOTransform file has the following order: [Top left corner X, cell size, 0,Top left corner Y, 0,
     -cell size]

    Args:
    -----------------------------------
    :param file_path: string with path where a .txt ASCII raster file is located

    :return: tuple with GEOtransform raster information, df with ASCII file header (to later save the results), and
    float with nodata value
    """
    # Save the ASCII raster information into a pandas data frame. It will have the following order:
    # ncols, nrows, xllcorner, yllcorner, cellsize, nodata_value
    # IF DELIMITER AND DECIMAL SEPARATOR ARE NOT A SPACE AND A COMMA (respectively) CHANGE THE FOLLOWING LINE
    df_head = pd.read_csv(file_path, delimiter='\s+', header=None, nrows=6, decimal=",")
    # print("Header:\n", df_head)

    # Save info as an array to save the data as GEOtransform type
    info_array = np.array(df_head.iloc[:, 1])
    # print(info_array)

    # Save needed information to create a GEOtransform variable (Top left corner X, cell size, 0,Top left corner Y,
    # 0, -cell size)
    cell_size = float(info_array[4])  # Get cell size from the header information)
    ulx = float(info_array[2])  # Get Xmin (or ulx/llx) directly from the header information
    uly = float(info_array[3] + cell_size * info_array[1])  # Get uly by adding all the rows above the lly from the
    #                                                       # header information
    no_data = float(info_array[5])

    gt_array = [ulx, cell_size, 0.0, uly, 0.0, -cell_size]
    # print("GT: ", GT_array)
    gt = tuple(gt_array)  # Convert to type tuple to be read by save raster functions

    return gt, df_head, no_data


def get_array_ascii(file_path):
    """
    Function extracts the data from the ASCII .txt file (excluding the header)

    Args:
    --------------------------------
    :param file_path: path where a .txt ASCII raster file is located

    :return: array with the raster data (including no data values)
    """
    array = np.array(pd.read_csv(file_path, delimiter='\s+', header=None, skiprows=6, decimal=","))
    # print("First value: ", array[1][660])

    return array


def get_raster_data(raster_path, data_info):
    """
    Function gets GEOTransform (gt) and projection data from a .tif raster file

    Args:
    ----------------------------------------
    :param raster_path:  string with path where a .tif or other raster file format is located
    :param data_info: a boolean variable that is true if all information is needed, or false if only the projection is
    needed

    :return: tuple gt with GEOTransform and tuple with raster projection
    """
    raster = gdal.Open(raster_path)  # Extract raster from path
    gt = raster.GetGeoTransform()  # Get Geotransform Data: Coordinate left upper corner, cellsize, 0, Coord. Lower
    # right corner, 0, cell size
    proj = raster.GetProjection()  # Get projection of raster

    band = raster.GetRasterBand(1)  # Get raster band (the 1st one, since the inputs have only 1)
    no_data = np.float32(band.GetNoDataValue())  # Get NoData value

    if data_info:
        return gt, proj, no_data  # Return both variables
    else:
        return proj


def save_raster(array, output_path, gt, proj):
    """
    Function saves an array to a .tif raster file format. The nodata values should be -9999.

    Args:
    ---------------------------------------
    :param array: array with results to save to a .tif raster file
    :param output_path: path and file name with which to save the .tif raster file
    :param gt: GEOTransform data
    :param proj: raster projection

    """
    # Step 1: Get drivers in order to save outputs as raster .tif files
    driver = gdal.GetDriverByName("GTiff")  # Get Driver and save it to variable
    driver.Register()  # Register driver variable

    # #Step 2: Create the raster files to save, with all the data: folder + name, number of columns (x),
    # number of rows (y), No. of bands, output data type (gdal type)
    outrs = driver.Create(output_path, xsize=array.shape[1], ysize=array.shape[0], bands=1, eType=gdal.GDT_Float32)

    # Step 3: Assign raster data and assaign the array to the raster
    outrs.SetGeoTransform(gt)  # assign geo transform data from the original input raster (same size)
    outrs.SetProjection(proj)  # assign projection to raster from original input raster (same projection)
    outband = outrs.GetRasterBand(1)  # Create a band in which to input our array into
    outband.WriteArray(array)  # Read array into band
    # outband.SetNoDataValue(np.nan)  # Set no data value as Numpy nan
    outband.SetNoDataValue(-9999.0)  # Set no data value as Numpy nan
    outband.ComputeStatistics(0)  # Set the raster statistics to the output raster

    # Step 4: Save raster to folder
    outband.FlushCache()
    outband = None
    outrs = None

    print("Saved raster: ", os.path.basename(output_path))
