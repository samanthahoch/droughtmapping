
import os, tempfile
import shutil

import json
from urllib import request
from datetime import date
from datetime import timedelta
from osgeo import gdal
import numpy as np
import arcpy

today = date.today().strftime("%Y%m%d")
data_date = (date.today() - timedelta(days = 1)).strftime("%Y%m%d")

url = ("https://www1.ncdc.noaa.gov/pub/data/nidis/geojson/us/soil/SManom_current.geojson")

write_folder = "C:/Users/samihoch/" + today
os.mkdir(write_folder)

arcpy.management.CreateFileGDB(write_folder, "Drought.gdb")
arcpy.env.workspace = os.path.join(write_folder, "Drought.gdb")

blank_map = "C:/Users/samihoch/BlankMap/BlankMap.aprx"
shutil.copyfile(blank_map, write_folder + "/DroughtMap.aprx")

write_filename = write_folder + "/Drought.gdb/most_recent.geojson"
response = request.urlretrieve(url, write_filename)

print("Downloading data from noaa")

json_file = open(write_filename)
data_raw = json.load(json_file)

with open(write_filename) as json_file:
    data_raw = json.load(json_file)

if not os.path.exists('C:\Temp'):
    os.makedirs('C:\Temp')

arcpy.management.CreateFileGDB(r'C:\Temp', 'Live.gdb')
arcpy.env.workspace = os.path.join(r'C:\Temp', 'Live.gdb')
data_areas = dict(type=data_raw['type'], features=[])

print("Reading json data")

for feat in data_raw['features']:
    data_areas['features'].append(feat)

areas_json_path = os.path.join(r'C:\Temp', 'polygons.json')

# Save dictionaries into json files
with open(areas_json_path, 'w') as poly_json_file:
    json.dump(data_areas, poly_json_file, indent=4)

print("json file saved to: ", write_folder + "/Drought.gdb/polygons.json")






