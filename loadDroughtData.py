import arcpy
import os, tempfile
from datetime import date

today = date.today().strftime("%Y%m%d")
write_folder = "C:/Users/samihoch/" + today

aprx = arcpy.mp.ArcGISProject(write_folder + "/DroughtMap.aprx")
aprx.defaultGeodatabase = write_folder + r"/Drought.gdb"

areas_json_path = os.path.join(r'C:\Temp', 'polygons.json')

arcpy.conversion.JSONToFeatures(r"C:\Temp\polygons.json",
 write_folder + "\Drought.gdb\drought_areas", "POLYGON")

arcpy.conversion.FeatureClassToFeatureClass("drought_areas", write_folder + "\Drought.gdb", "drought_areas_save", '', 'VALUE "VALUE" true true false 8000 Text 0 0,First,#,alert_areas,VALUE,0,8000;AREA "AREA" true true false 8 Double 0 0,First,#,alert_areas,AREA,-1,-1;CONUS_AREA "CONUS_AREA" true true false 8 Double 0 0,First,#,alert_areas,CONUS_AREA,-1,-1;CONUSPRCNT "CONUSPRCNT" true true false 8 Double 0 0,First,#,alert_areas,CONUSPRCNT,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,alert_areas,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,alert_areas,Shape_Area,-1,-1', '')

arcpy.management.MultipartToSinglepart("drought_areas_save",
 write_folder + "\Drought.gdb\drought_split")

arcpy.mp.ArcGISProject(write_folder + "/DroughtMap.aprx").save()

m = aprx.listMaps('Map')[0]

polygons_lyr = m.listLayers('drought_split')[0]
polygons_sym = polygons_lyr.symbology

arcpy.AddField_management("drought_split", "DoubleVal", "DOUBLE")
arcpy.management.CalculateField("drought_split", "DoubleVal", "!VALUE!", "PYTHON3", '')


# save layer and apply symbology from layer 

