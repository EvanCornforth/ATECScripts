# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:24:43 2017

@author: arevill
"""

GPSFile = '//csce.datastore.ed.ac.uk/csce/geos/groups/ATEC/DATA/WK/field_scale/WK_F1_2017/field_scale_data/seagul_gps/20170831/Flight9/GPS.txt'
newGPSCSVFilename = GPSFile[:-4] + "Times.csv"
directory = "//csce.datastore.ed.ac.uk/csce/geos/groups/ATEC/DATA/WK/field_scale/WK_F1_2017/field_scale_data/sony_rgb/20170831/flight3"


import os
from PIL import Image 
from PIL.ExifTags import TAGS

fileHolder = []
fileCounter = 0
for file in os.listdir(directory):
    if file.endswith(".JPG"):
        fileHolder.append(os.path.join(directory, file))
        fileCounter = fileCounter + 1
print("Found %d images in directory %s" % (fileCounter, directory))

exifTimes = []
for i in range(fileCounter):
        image = Image.open(fileHolder[i])
        info = image._getexif() 
        cnt = 0
        for tag, value in info.items():
            cnt = cnt + 1
            if cnt == 16:
                key = TAGS.get(tag, tag) 
                exifTimes.append(str(value[-8:]))

with open(GPSFile, 'r') as jpgFile:
    jpgFileLines = jpgFile.read().split("\n")
    GPStimes = [(jpgFileLines[x]).split(',')[1] for x in range(0, len(jpgFileLines)-1)]

seconds = []
for i in range(len(GPStimes)):
    seconds.append(float(GPStimes[i][:2])*60*60 + float(GPStimes[i][2:4])*60 + float(GPStimes[i][4:6]) + float(GPStimes[i][-2:])*0.01)

exifSeconds = []    
for i in range(len(exifTimes)):
    exifSeconds.append(float(exifTimes[i][:2])*60*60 + float(exifTimes[i][3:5])*60 + float(exifTimes[i][6:]))

for i in range(fileCounter-len(GPStimes)):
    seconds.append("0")
for i in range(len(GPStimes)-fileCounter):
    exifSeconds.append("0")

with open(newGPSCSVFilename, 'w') as newFile:
    firstRow = "Exif Seconds" + "," + "GPS Seconds" + "\n"
    newFile.write(firstRow)
    for i in range(len(seconds)):
        row = str(exifSeconds[i]) + "," + str(seconds[i]) + "\n"
        newFile.write(row)
        
print("All done :)")