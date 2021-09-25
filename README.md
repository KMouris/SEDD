# Sum pixel values upstream along a flow path

# Introduction
The code sums up the pixel values of an input raster along a flow path in upstream direction.
It can be used to calculate the travel time of eroded particles to the river network or catchment outlet based on the pixel-specific travel time according to [Jain and Kothyari (2000)](https://www.tandfonline.com/doi/pdf/10.1080/02626660009492376?needAccess=true). 
It works principally for each eight direction flow model (D8). Here the flow direction is defined
according to [Jenson & Domingue 1998](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-flow-direction-works.htm) which is the usual definition in GIS programs.

## Libraries

*Python* libraries:  *gdal*, *numpy*, *pandas*

*Standard* libraries: *glob*, *os*, *sys*, *time*

## Input

| Input argument | Type | Description |
|-----------------|------|-------------|
|`flowdir_path`| STRING | path for the flow direction raster (D8) (in .txt ASCII file format or raster format)|
|`traveltime_path`| STRING | path for the raster to be summed up along the flow path (here travel time) (in .txt ASCII file format or raster format)  |
|`proj_raster`| STRING | path for the projection raster (program gets the raster projection, in case both input rasters are in .txt format) (.tif format)  |
|`results_path`| STRING | Path of the result folder |

## Output

**Result folder:** 

`TotalTravelTime.tif` raster file (.tif) which contains the travel time of the eroded particles to the river network as pixel values.

## Code Diagram
![sedd_diagram](https://user-images.githubusercontent.com/65073126/134777833-f2805ec7-9431-4e5f-ba08-a0b2b2945623.jpg)

![sedd_diagram](Diagrams/sedd_diagram.jpg
