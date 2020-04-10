import arcpy
import shutil
import os, tempfile
from datetime import date

# create variables for today's date, write folder, and geoDatabase
today = date.today().strftime("%Y%m%d")
write_folder = "C:/Users/samihoch/" + today
geoDatabase = write_folder + r"/Drought.gdb"

# set the map that everything will be done on to the current open map
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprx.defaultGeodatabase = geoDatabase

# add the json data to the map
print("Adding json data to map")
areas_json_path = os.path.join(r'C:\Temp', 'polygons.json')

arcpy.conversion.JSONToFeatures(r"C:\Temp\polygons.json",
 geoDatabase + r"\drought_areas", "POLYGON")

# delete the temp folder
shutil.rmtree('C:\Temp')

# clean up the drought data
print("Preparing drought map features")

arcpy.conversion.FeatureClassToFeatureClass("drought_areas",
 geoDatabase, "drought_areas_save", '',
  'VALUE "VALUE" true true false 8000 Text 0 0,First,#,alert_areas,VALUE,0,8000;AREA "AREA" true true false 8 Double 0 0,First,#,alert_areas,AREA,-1,-1;CONUS_AREA "CONUS_AREA" true true false 8 Double 0 0,First,#,alert_areas,CONUS_AREA,-1,-1;CONUSPRCNT "CONUSPRCNT" true true false 8 Double 0 0,First,#,alert_areas,CONUSPRCNT,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,alert_areas,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,alert_areas,Shape_Area,-1,-1', '')

arcpy.management.MultipartToSinglepart("drought_areas_save",
 geoDatabase + r"\drought_split")

aprx.save()

# apply symbology from a previously save layer
print("Applying symbology")

m = aprx.listMaps('Map')[0]

polygons_lyr = m.listLayers('drought_split')[0]
polygons_sym = polygons_lyr.symbology

# add a new field to house the soil value as a double instead of a text value
arcpy.AddField_management("drought_split", "SoilValue", "DOUBLE")
arcpy.management.CalculateField("drought_split", "SoilValue", "!VALUE!", "PYTHON3", '')

arcpy.management.ApplySymbologyFromLayer(r"C:\Users\samihoch\drought_sym.lyrx", 
"drought_split", "VALUE_FIELD SoilValue SoilValue", "DEFAULT")

# rename to appropiate names
l = m.listLayers("drought_split")[0]
l.name = "Soil Moisture"

# remove all layers that are no longer needed
to_remove = ["drought_areas", "drought_areas_save", "drought_split"]

for i in to_remove:
    layer_remove = m.listLayers(i)[0]
    m.removeLayer(layer_remove)

aprx.save()

print("Successfully completed loadDroughtData script")


