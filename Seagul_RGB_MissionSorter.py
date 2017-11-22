# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:08:10 2017

@author: arevill
"""

GPSFile = '//csce.datastore.ed.ac.uk/csce/geos/groups/ATEC/DATA/WK/field_scale/WK_F1_2017/field_scale_data/seagul_gps/20170831/Flight9/GPS.txt'
newGPSCSVFilename = GPSFile[:-4] + "Data.csv"
directory = "//csce.datastore.ed.ac.uk/csce/geos/groups/ATEC/DATA/WK/field_scale/WK_F1_2017/field_scale_data/sony_rgb/20170831/flight3"
newPath = 'C:/Users/arevill/Documents/EvanStuff/Flight3/'

import os
from shutil import copy

filePathHolder = []
fileNameHolder = []
fileCounter = 0
for file in os.listdir(directory):
    if file.endswith(".JPG"):
        filePathHolder.append(os.path.join(directory, file))
        fileNameHolder.append(file)
        fileCounter = fileCounter + 1
print("Found %d images in directory %s" % (fileCounter, directory))

with open(GPSFile, 'r') as gpsFile:
    gpsFileLines = gpsFile.read().split("\n")
    del gpsFileLines[-1]
    
#For Flight 1
#listOfSeagulDataToDel = [8, 7, 6, 5, 4, 3, 2, 1, 0]
#listOfRGBDataToDel = []

#For Flight 2
#listOfSeagulDataToDel = [-1]
#listOfRGBDataToDel = [-1, 190, 41]

#For Flight 3
listOfSeagulDataToDel = []
listOfRGBDataToDel = [-1, 254, 212, 191, 118, 106, 91, 51, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

for elem in listOfRGBDataToDel:
    del filePathHolder[elem]
    del fileNameHolder[elem]

for elem in listOfSeagulDataToDel:
    del gpsFileLines[elem]
    
GPSFileLats = [(gpsFileLines[x]).split(',')[2] for x in range(0, len(gpsFileLines))]
GPSFileLongs = [(gpsFileLines[x]).split(',')[4] for x in range(0, len(gpsFileLines))]
GPSAlts = [(gpsFileLines[x]).split(',')[9] for x in range(0, len(gpsFileLines))]

GPSLats = [str(float(elem[:2]) + float(elem[2:])/60.0) for elem in GPSFileLats]
GPSLongs = [str(float(elem[:3]) + float(elem[3:])/60.0) for elem in GPSFileLongs]


if len(gpsFileLines) == len(filePathHolder):
    print(len(gpsFileLines), len(filePathHolder))
    with open(newGPSCSVFilename, 'w') as newFile:
        firstRow = "Image Name" + "," + "Latitude" + "," + "Longitude" + "," + "Altitude" + "\n"
        newFile.write(firstRow)
        for i in range(len(gpsFileLines)):
            row = fileNameHolder[i] + "," + GPSLats[i] + "," + GPSLongs[i] + "," + GPSAlts[i] + "\n"
            newFile.write(row)
else:
    print("Something went wrong :(")
    print(len(gpsFileLines), len(filePathHolder))
    
print("GPS data file created at: ", newGPSCSVFilename)
    
for i in range(len(gpsFileLines)):
    copy(filePathHolder[i], newPath + fileNameHolder[i])
    if i%5 == 0:
        print("Moved JPG %d out of %d" % (i, len(gpsFileLines)))
 
print("All %d JPSs moved to their new folder at: %s" % (len(gpsFileLines), newPath))

print("All done :)")


