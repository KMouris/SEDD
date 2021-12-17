# Sum Up Pixel Values Along a Flow Path for SEDD

# Introduction
The algorithms provided with this repository sum up pixel values of an input raster along a (flow) path in upstream direction. The (flow) direction is determined based on a flow direction *GeoTIFF* raster. The primary development goal of the algorithms were to calculate the travel time of eroded particles of a river network or catchment outlet based on a pixel-specific travel time according to [Jain and Kothyari (2000)](https://www.tandfonline.com/doi/pdf/10.1080/02626660009492376?needAccess=true). This technique works semantically with any eight-directional flow model (D8). Here, the flow direction is defined according to [Jenson & Domingue 1998](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-flow-direction-works.htm), which is typically also used in GIS programs, such as [QGIS](https://qgis.org).


## Requirements

The algorithms are written in Python3 ([get installation instructions](https://hydro-informatics.com/python-basics/pyinstall.html)) and build on the following external libraries:  *gdal*, *numpy*, *pandas*

In addition, the following standard Python libraries are used: *glob*, *os*, *sys*, *time*

## Input

The below-listed input arguments and data have to be provided to run the algorithms. The input arguments are variables that can be set in `ROOT/config.py`.

| Input argument | Type | Description |
|----------------|------|-------------|
|`flowdir_path`| *string* | path for the flow direction raster (D8) (in .txt ASCII file format or raster format)|
|`traveltime_path`| *string* | path for the raster to be summed up along the flow path (here travel time) (in .txt ASCII file format or raster format)  |
|`proj_raster`| *string* | path for the projection raster (program gets the raster projection, in case both input rasters are in .txt format) (.tif format)  |
|`results_path`| *string* | Path of the result folder |

## Output

**Result folder:** `TotalTravelTime.tif` raster file (.tif) which contains the travel time of the eroded particles to the river network as pixel values.

## Code Diagram
![](diagrams/sedd_diagram.jpg)

# Disclaimer

No warranty is expressed or implied regarding the usefulness or completeness of the information and documentation provided. References to commercial products do not imply endorsement by the Authors. The concepts, materials, and methods used in the algorithms and described in the documentation are for informational purposes only. The Authors has made substantial effort to ensure the accuracy of the algorithms and the documentation, but the Authors shall not be held liable, nor his employer or funding sponsors, for calculations and/or decisions made on the basis of application of the scripts and documentation. The information is provided "as is" and anyone who chooses to use the information is responsible for her or his own choices as to what to do with the data. The individual is responsible for the results that follow from their decisions.

This web site contains external links to other, external web sites and information provided by third parties. There may be technical inaccuracies, typographical or other errors, programming bugs or computer viruses contained within the web site or its contents. Users may use the information and links at their own risk. The Authors of this web site excludes all warranties whether express, implied, statutory or otherwise, relating in any way to this web site or use of this web site; and liability (including for negligence) to users in respect of any loss or damage (including special, indirect or consequential loss or damage such as loss of revenue, unavailability of systems or loss of data) arising from or in connection with any use of the information on or access through this web site for any reason whatsoever (including negligence).


# Authors

- Kilian Mouris
- Maria Fernanda Morales Oreamuno
- Sebastian Schwindt
