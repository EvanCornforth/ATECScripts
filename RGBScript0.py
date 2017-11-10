# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:23:43 2017
Takes in all jpgs in a directory, reads their exif data and then creates a new 
csv file with columns of Image Name / Time Taken / Date Taken

@author: Evan
"""

directoryInput = input('Enter the directory of JPG images: ')
directory = directoryInput.replace("\\", "/")
outputFilename = directory+'/JPGImageTimes.csv'
offsetSecs = int(input('Enter the JPG offset from GPS time in seconds: '))

import os
from PIL import Image 
from PIL.ExifTags import TAGS

fileHolder = []
fileCounter = 0
for file in os.listdir(directory):
    if file[-3:].lower() == "jpg":
        fileHolder.append(os.path.join(directory, file))
        fileCounter = fileCounter + 1
print("Found %d images in directory %s" % (fileCounter, directory))

def howManySecs(clockFace):
    secs = int(clockFace[-2:]) + 60*int(clockFace[3:5]) + 60*60*int(clockFace[:2])
    return secs
        
with open(outputFilename, 'w') as outputFile:
    firstRow = "Image Name" + "," + "Time Taken" + "," + "Total Seconds" + "," + "Date Taken" + "\n"
    outputFile.write(firstRow)
    for i in range(fileCounter):
        image = Image.open(fileHolder[i])
        info = image._getexif()
        string = "DateTimeOriginal"
        for tag, value in info.items(): 
            key = TAGS.get(tag, tag)
            #print(key + " " + str(value))  #Would print out all exif data
            if key == string:
                row = fileHolder[i] + "," + str(value[-8:]) + "," + str(howManySecs(value[-8:])-offsetSecs) + "," + str(value[0:10]) + "\n"
                outputFile.write(row)

image.close()
print("Output csv file for jpg image times created at location:", outputFilename)

with open(directory+'/SummaryFlightFile.csv', 'r') as inputFlightFile:
        missionLines = inputFlightFile.read().split("\n")
        
with open(directory+'/JPGImageTimes.csv', 'r') as inputjpgFile:
        jpgLines = inputjpgFile.read().split("\n")
        
missionSeconds = [float((missionLines[x]).split(',')[0]) for x in range(2, len(missionLines)-1)]
intMissionSeconds = [int(missionSeconds[x]) for x in range(len(missionSeconds))]
longitudes = [(missionLines[x]).split(',')[1] for x in range(2, len(missionLines)-1)]
latitudes = [(missionLines[x]).split(',')[2] for x in range(1, len(missionLines)-1)]
altitudes = [(missionLines[x]).split(',')[3] for x in range(1, len(missionLines)-1)]
jpgImageNames = [(jpgLines[x]).split(',')[0] for x in range(1, len(jpgLines)-1)]
jpgSeconds = [int((jpgLines[x]).split(',')[2]) for x in range(1, len(jpgLines)-1)]

cnt = 0
jpgSecondsLineNum = []

#This for loop will compare the jpg exif times in seconds with that of the
#mission times in seconds, if there are matches it
#Will find 46 in 746 btw so be carfeul!!!!!
cnt2 = 0
cnt3 = 0
for sec in jpgSeconds:
    cnt = 0
    cnt3 = cnt3 + 1
    while cnt==0:
        try:
            jpgSecondsLineNum.append(intMissionSeconds.index(sec))
            break
        except ValueError:
            cnt = cnt + 1
            cnt2 = cnt2 + 1
            jpgSecondsLineNum.append(0)            

print("Matched %d JPGs to the flight file with their line number is listed below" % (cnt3-cnt2))
print(jpgSecondsLineNum) 
    
with open(directory+'/FinalMissionData.csv', 'w') as jpgFinalDataFile:
    firstRow = "File Name" + "," + "Longitude" + "," + "Latitude" + "," + "Altitude" + "\n"
    jpgFinalDataFile.write(firstRow)
    for i in range(len(jpgSeconds)):
        lineNum = jpgSecondsLineNum[i]
        if lineNum != 0:
            if lineNum >= missStartLine and lineNum <= missEndLine:
                row = jpgImageNames[i] + "," + longitudes[lineNum] + "," + latitudes[lineNum] + "," + altitudes[lineNum] + "\n"
                jpgFinalDataFile.write(row)

print("Written CSV file of images from this flight and on mission to location:", directory+'/FinalMissionData.csv')
            
with open(directory+'/FinalNotMissionData.csv', 'w') as jpgFinalDataFile:
    firstRow = "File Name" + "\n"
    jpgFinalDataFile.write(firstRow)
    for i in range(len(jpgSeconds)):
        lineNum = jpgSecondsLineNum[i]
        if lineNum != 0:
            if lineNum <= missStartLine or lineNum >= missEndLine:
                row = jpgImageNames[i] + "\n"
                jpgFinalDataFile.write(row)
        if type(lineNum) != int and type(lineNum) != float:
            row = jpgImageNames[i] + "\n"
            jpgFinalDataFile.write(row)
            
print("Written CSV file of images from this flight but not on mission to location:", directory+'/FinalNotMissionData.csv')