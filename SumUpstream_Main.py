import numpy as np
import pandas as pd
import gdal
import os
import glob
import sys
import time

import SumUpstream_ReadDataFunctions as ReadData
import SumUpstream_SaveFunctions as SaveData

# ---------------------------------------------FUNCTIONS------------------------------------------------------------- #

# ------Functions: Save Results ------------------------------------------------------------------------------------- #




# ---------------------------------------------USER INPUT------------------------------------------------------------ #
"""
Program is translated from the R code called "SumUpstream.R", which sums up the cells of an input Raster 
(e.g. travel time per cell) in upstream direction
Important information: 
    -Works for each eight-direction (D8) flow model, here the flow directions are defined according to Jenson & 
     Domingue 1998 (ArcGIS)
    -Requires 2 input rasters: Flow direction and file with data to sum in the upstream direction 
    -Both rasters have to have the same properties (same number of columns, rows and georeferencing)
    -Rasters can be in .txt (ASCII format) or in .tif format
    - If the rasters are in ASCII format: the comma delimiter must be a comma and the delimiter must be a space 
        (if not, change the pd.read_csv input data in the functions "GetASCII_Info" and "GetArray_ASCII")
"""

start_time = time.time()

# 1. Flow direction raster (in .txt ASCII file format or raster format)
flowdir_path = r'Y:\Abt1\hiwi\Oreamuno\Tasks\Code_translation\RCode\Input_data_2test\fl_dir_4000.txt'

# 2. Travel time (per cell) raster (in .txt ASCII file format or raster format)
traveltime_path = r'Y:\Abt1\hiwi\Oreamuno\Tasks\Code_translation\RCode\Input_data_2test\traveltime_percell_corr.txt'

# 3. Projection raster: in case both input rasters are in .txt format (program gets the raster projection)
proj_raster = r'Y:\Abt1\hiwi\Oreamuno\SY_062016_082019\Rasters\fildemBanja.tif'

# 4. Results path
results_path = r'P:\aktiv\2018_DLR_DIRT-X\300_Modelling\340 Evaluation\Python Codes\Sum_upstream\Python_Results'


# ----------------------------------------- MAIN CODE --------------------------------------------------------------- #

# -------Read Data: ------------------------------------------------------------------------------------------------- #


if os.path.splitext(flowdir_path)[1] == ".txt":  # If flowdir raster is in ASCII format
    # Get gt, raster header and no data value information
    gt, df_head, no_data = ReadData.GetASCII_Info(flowdir_path)
    # save data to an array
    flowdir_array = ReadData.GetArray_ASCII(flowdir_path)
else: # If flowdir raster is in .tif or other raster format
    # Get gt, projection and no data value information
    gt, proj, no_data = ReadData.GetRasterData(flowdir_path, True)

if os.path.splitext(traveltime_path)[1] == ".txt":  # If traveltime raster is in ASCII format
    ttime_array = ReadData.GetArray_ASCII(traveltime_path)
else:  # If traveltime raster is in .tif or other raster format
    print("No function yet for .tif files ")

# If both input rasters are in .txt format, get the projection data from a third input raster (to later save the raster
# as a .tif format raster)
if os.path.splitext(flowdir_path)[1] == ".txt" and os.path.splitext(traveltime_path)[1] == ".txt":
    proj = ReadData.GetRasterData(proj_raster, False)

# -------Generate result rasters ------------------------------------------------------------------------------------ #
total_ttime = np.full((flowdir_array.shape[0], flowdir_array.shape[1]), no_data)
# ------------------------------------------------------------------------------------------------------------------- #

end_reading_time = time.time()
print("Reading data took: ", end_reading_time-start_time)

# ------- LOOPS ----------------------------------------------------------------------------------------------------- #.

# Loop 1 and 2: Loop through each cell in the flowdir raster:
for i in range(0, flowdir_array.shape[0]):  # Loop through rows
    for j in range(0, flowdir_array.shape[1]):  # Loop through columns
        # Only do calculations if both flowdir and traveltime rasters have values in cell [i,j]
        if flowdir_array[i][j] != no_data and ttime_array[i][j] != no_data:
            # print("Starting the cell: [", i, ",", j, "]" )
            # Cell [i,j] is our starting point, so save coordinates to variables x, y
            x = j  # Columns (j) are equivalent to changes in X
            y = i  # rows (i) are equivalent to changes in Y
            value = 0  # Initialize a variable in which to save the sum of travel time, in the upstream direction

            loopstart_time = time.time()

            # Sum the travel time for each cell [i,j], moving in the direction of the flow downstream.
            while 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                # print("Next while loop starting for cell: [", i, ",", j, "]")
                # If flowdir[y,x] is a nodata value cell (river), then exit the while loop and into the next for loop
                if flowdir_array[y][x] == no_data:
                    # print("The following cell has a no data value: ", x, ",", y)
                    break
                else:
                    # Start reading the content of each cell [y,x]
                    if flowdir_array[y][x] == 1:  # Direction is E
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X value only
                        x = x + 1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 16:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 2:  # Direction is diagonal E-S
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 2")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X and Y values
                        x = x + 1
                        y = y+1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 32:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 4:  # Direction is S
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 4")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update Y value only
                        y = y+1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 64:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 8:  # Direction is diagonal S-W
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 8")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X and Y values
                        x = x-1
                        y = y+1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 128:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 16:  # Direction is W
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 16")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X value only
                        x = x-1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 1:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 32:  # Direction is diagonal: N-W
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 32")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X and Y values
                        x = x-1
                        y = y-1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 2:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 64:  # Direction is: N
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 64")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update Y value only
                        y = y-1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 4:  # If the next cell returns to previous cell (loop)
                                break
                    elif flowdir_array[y][x] == 128:  # Direction is diagonal: N-E
                        # print("Cell coordinates: [", y, ",", x, "] for flow direction type 128")
                        value = value + ttime_array[y][x]  # Add travel time in cell [y,x] to total travel time
                        # Update X and Y values
                        x = x+1
                        y = y-1
                        # If the updated [y,x] coordinate is still inside the original flowdir raster:
                        if 0 <= x < flowdir_array.shape[1] and 0 <= y < flowdir_array.shape[0]:
                            if flowdir_array[y][x] == no_data:  # If the next cell is a no data cell (reached a river)
                                break
                            if flowdir_array[y][x] == 8:  # If the next cell returns to previous cell (loop)
                                break

            # Save the sum of the travel time of each cell in the results array for cell [i,j]
            total_ttime[i][j] = value

            # If the total value is negative (summed a no data value) then make value as no data
            if total_ttime[i][j] < 0:
                total_ttime[i][j] = no_data

            loopend_time = time.time()
            # print("Loop with cell [", i, ",", j, "] took: ", loopend_time-loopstart_time, " seconds")


# ------- Save results:  -------------------------------------------------------------------------------------------- #

# save_name = results_path + "\\Flowdir.tif"
# SaveRaster(flowdir_array, save_name, gt, proj)

save_name = results_path + "\\TotalTravelTime.tif"
SaveData.SaveRaster(total_ttime, save_name, gt, proj)

print("Program took ", time.time() - start_time, " seconds to run")