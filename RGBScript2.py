# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:02:12 2017

@author: Evan
"""

directoryInput = input('Enter the directory of JPG images: ')
directory = directoryInput.replace("\\", "/")
missStartLine = 5963	
missEndLine = 8052


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