<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 09:35:25 2017

@author: arevill
"""

import os
from tkinter.filedialog import askdirectory

#imageDirectoryInput = input('Enter the image directory: ')
#imageDirectory = imageDirectoryInput.replace("\\", "/")
imageDirectory = askdirectory()
#maiaLogPathInput = input('Enter the MAIA log path: ')
#maiaLogPath = maiaLogPathInput.replace("\\", "/")
maiaLogPath = askdirectory()

missionSpeed = []
missionSpeedBumpiness = []
missionAlt = []
missionAltBumpiness = []

errMsg = "ERROR FETCHING DATA"
newpath3 = imageDirectory + '/FlightErrorData'
if not os.path.exists(newpath3):
    os.makedirs(newpath3)

fileHolder = []
fileNameHolder = []
fileCounter = 0
for file in os.listdir(maiaLogPath):
    if file.endswith(".log"):
        fileHolder.append(os.path.join(imageDirectory, file))
        fileNameHolder.append(file)
        fileCounter = fileCounter + 1
print("Found %d log files in directory %s" % (fileCounter, maiaLogPathInput))

for logs in fileHolder:
    print(logs)
    missionSpeed.append(float(input('Enter the mission speed:')))
    missionSpeedBumpiness.append(float(input('Enter the mission speed bumpiness:')))
    missionAlt.append(float(input('Enter the mission alt:')))
    missionAltBumpiness.append(float(input('Enter the mission alt bumpiness:')))

fileData = []

for i in range(fileCounter):
    missStartLine = 0
    missEndLine = 0
    newpath1 = imageDirectory + '/Flight' + str(i+1) + 'MissionData'  
    newpath2 = imageDirectory + '/Flight' + str(i+1) + 'NotMissionData'  
    outputFileName = newpath1 + '/MissionOnlyMaiaLog.csv'
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
    if not os.path.exists(newpath2):
        os.makedirs(newpath2)
        
    with open(fileHolder[i]) as file:
        fileLines = file.read().split("\n") 
        
        noDataImgs = []
        fileLineDels = []       
        for j,line in enumerate(fileLines):
            if errMsg in line:
                noDataImgs.append((fileLines[j]).split('\t')[3])
                fileLineDels.append(j)
                
        fileLineDels.reverse()
        for elem in fileLineDels:
            del fileLines[elem]
            
        fileImageNames = [(fileLines[x]).split('\t')[3] for x in range(len(fileLines)-1)]
        fileSpeeds = [(fileLines[x]).split('\t')[14] for x in range(len(fileLines)-1)]
        fileAltitudes = [(fileLines[x]).split('\t')[11] for x in range(len(fileLines)-1)]
        fileLongs = [(fileLines[x]).split('\t')[7] for x in range(len(fileLines)-1)]
        fileLats = [(fileLines[x]).split('\t')[9] for x in range(len(fileLines)-1)]
        newFileImageNames = [0 for x in range(len(fileLines)-1)]
        newFileImageNames[0] = fileImageNames[0]
        for a in range(1, len(fileLines)-1):
            newFileImageNames[a] = fileImageNames[a][:-3] + 'tif'
        missionAlts = []
        
        def speedChecker(vals, heightVals):
            cnt = 0
            for val in vals:
                if missionSpeed[i] - missionSpeedBumpiness[i] < val < missionSpeed[i] + missionSpeedBumpiness[i]:
                    cnt = cnt + 1
            if cnt == len(vals):
                if altitudeChecker(heightVals) == 1:
                    return 1
                else:
                    return 0
            else: 
                return 0

        def altitudeChecker(vals):  
            cnt = 0
            for val in vals:
                if missionAlt[i] - missionAltBumpiness[i] < val < missionAlt[i] + missionAltBumpiness[i]:
                    cnt = cnt + 1
            if cnt == len(vals):
                return 1
            else: 
                return 0
    
        check = 0
        counter = 1
        while check == 0:
            if counter >= (len(fileLines) - 32):
                missStartLine = 0
                break
            speedVals = [float(fileSpeeds[x]) for x in range(counter, counter+30)]
            heightVals = [float('0' + fileAltitudes[x]) for x in range(counter, counter+30)]
            counter = counter + 1
            check = speedChecker(speedVals, heightVals)
            missStartLine = counter
        print("Mission start line is:", missStartLine)

        check = 0
        counter = len(fileLines) - 1
        while check == 0:
            if counter <= 32:
                missEndLine = 0
                break
            speedVals = [float(fileSpeeds[x]) for x in range(counter-30, counter)]
            heightVals = [float('0' + fileAltitudes[x]) for x in range(counter-30, counter)]
            counter = counter - 1
            check = speedChecker(speedVals, heightVals)
            missEndLine = counter
        print("Mission end line is:", missEndLine)
        
        missionAlts = [c for c in range(missStartLine, missEndLine)]
        fileData.append((fileHolder[i], missStartLine, missEndLine))
        
        #Let the user know this flight has no mission images in it
        if len(missionAlts) == 0:
            print(fileHolder[i] + " has no mission data in it")
        
        #If the flight does have mission images, move them to the MissionData folder
        if len(missionAlts) != 0:
            for j in range(fileData[i][1], fileData[i][2]+1):
                os.rename(imageDirectory + '/' + fileImageNames[j],  newpath1 + '/' + fileImageNames[j])
        print("Moved all the on mission images from flight %d to their MissionData folder" % i)
        
        #Will move not mission images into the NotMissionData folder
        #Works if all images from flight are not mission data
        for a in range(1, fileData[i][1]):
            os.rename(imageDirectory + '/' + fileImageNames[a],  newpath2 + '/' + fileImageNames[a])
        for b in range(fileData[i][2]+1, len(fileImageNames)):
            os.rename(imageDirectory + '/' + fileImageNames[b],  newpath2 + '/' + fileImageNames[b])
        print("Moved all the not on mission images from flight %d to their NotMissionData folder" % i)
        
        if len(noDataImgs) != 0:
            newpath4 = newpath3 + '/Flight' + str(i+1) + 'ErrorData'
            if not os.path.exists(newpath4):
                os.makedirs(newpath4)
            for elem in noDataImgs:
                os.rename(imageDirectory + '/' + elem, newpath4 + '/' + elem)
        print("Moved all the images with MAIA erros to their ErrorData folder for flight %d" % i)
        
        #Writes a csv file with all the needed flight information for the on 
        #mission data, and writes it to the correct MissionData folder
        with open(outputFileName, 'w') as outputMaiaFile:
            firstRow = str(newFileImageNames[0]) + "," + str(fileLongs[0]) + "," + str(fileLats[0]) + "," + str(fileAltitudes[0]) + "\n"
            outputMaiaFile.write(firstRow)
            for d in range(missStartLine, missEndLine + 1):
                row = newFileImageNames[d] + "," + '-' + fileLongs[d] + "," + fileLats[d] + "," + fileAltitudes[d] + "\n"
                outputMaiaFile.write(row)

print('\a')
print("All done :)")