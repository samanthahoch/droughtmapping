# Reproducible Modeling of Drought Areas using Arcpy 

To use python to create a map of drought regions in the U.S. follow the below directions.

## Downloading the Data

Run the script downloadData.py using the python command window. Note some of the built in file paths may need to be adjusted. 

`python "path-to/downloadData.py`

This will download today's data from [NOAA]("https://www1.ncdc.noaa.gov/pub/data/nidis/geojson/us/soil/SManom_current.geojson") and create a folder for today's map.

## Open the Map

The previous script created a map document in the folder for today's data. Open the map document called DroughtMap.aprx. The rest of the python code will be run from the python console within this map document.

## Load the Data

Add the drought data to the map using loadDroughtData.py. Use a text editor to open the script and copy everything. Paste into the python console in ArcGIS Pro and run.

