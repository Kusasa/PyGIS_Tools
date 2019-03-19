"""--------------------------------------------------------------------------
Script Name:      Polygon to Point Tool
Version:          1.1
Description:      Converts polygons to points and gives them ordered and 
                  unique identifiers:
                    - Exploding the multipart polygons,
                    - Creating unique polygon names(i.e. POL1, POL2,...),
                    - Converting the polygons to points,
                    - Creating unique and ordered point names within each 
                      corresponding polygon (i.e. POL21, POL22, POL23...).  
Created By:       Kusasalethu Sithole
Date:             2019-03-18
Last Revision:    2019-03-19
-----------------------------------------------------------------------------"""

import arcpy

arcpy.env.overwriteOutput = True

# Request input of target shapefile
polygon_layer = arcpy.GetParameterAsText(0)
polygon_singlepart_layer = polygon_layer[:-4] + '_sglprt' + polygon_layer[-4:]
points_layer = arcpy.GetParameterAsText(1)

#Exploding the multipart polygons
arcpy.MultipartToSinglepart_management(polygon_layer, polygon_singlepart_layer)

#Adding column for polygon naming
arcpy.AddField_management(polygon_singlepart_layer, "POLYGON_NO", "TEXT", "#", "#", 20, "#", "NULLABLE", "NON_REQUIRED", "#")

#Populating polygon naming column using numbering with POL code(i.e. POL1, POL2,...) and Ceating a list of POLYGON_NO values
try:
    number = 1
    polygon_numbers = []
    fid = 0
    fields = ("FID","POLYGON_NO")
    with arcpy.da.UpdateCursor(polygon_singlepart_layer, fields) as Cursor:   #@UndefinedVariable
            for row in Cursor:
                UpdateValue = 'POL' + str(number)
                polygon_numbers.append(UpdateValue)
                if row[0]==fid:
                    row[1] = UpdateValue
                Cursor.updateRow(row)
                fid += 1
                number += 1

    del Cursor
except:
    print(arcpy.GetMessages())

#Converting polygons to points
arcpy.FeatureVerticesToPoints_management(polygon_singlepart_layer,points_layer,"ALL")

#Adding column for point naming
arcpy.AddField_management(points_layer, "POINT_NO", "TEXT", "#", "#", 20, "#", "NULLABLE", "NON_REQUIRED", "#")

#Selecting and adding point number per polygon for each record
try:
    for index in range(len(polygon_numbers)):
        n = 1
        columns = ("POLYGON_NO","POINT_NO")
        with arcpy.da.UpdateCursor(points_layer, columns) as Cursor:   #@UndefinedVariable
            for record in Cursor:
                if record[0] == polygon_numbers[index]:
                    record[1] = record[0] + str(n)
                    Cursor.updateRow(record)
                    n += 1

    del Cursor
except:
    print(arcpy.GetMessages())
#delete intermediary polygon_singlepart_layer
arcpy.Delete_management(polygon_singlepart_layer)

print("Process Complete")