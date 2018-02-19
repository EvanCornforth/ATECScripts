# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from PIL import Image 
from PIL.ExifTags import TAGS
from tkinter.filedialog import askdirectory

#directoryInput = input('Enter the directory of JPG images from this day: ')
#directory = directoryInput.replace("\\", "/")
directory = askdirectory()
if directory[-1] != "/":
    directory = directory + "/"
outputFilename = directory+'JPGImageTimes.csv'

#####Changed
#offsetSecs = int(input('Enter the JPG offset from GPS time in seconds: '))
offsetSecs = 0

#flightLogDirectoryInput = input('Enter the directory containing the flight logs for this day: ')
#flightLogDirectory = flightLogDirectoryInput.replace("\\", "/")
flightLogDirectory = askdirectory()
if flightLogDirectory[-1] != "/":
    flightLogDirectory = flightLogDirectory + "/"

fileHolder = []
jpgCounter = 0
for jpgFile in os.listdir(directory):
    if jpgFile[-3:].lower() == "jpg":
        fileHolder.append(os.path.join(directory, jpgFile))
        jpgCounter = jpgCounter + 1
print("Found %d JPG images in directory: %s" % (jpgCounter, directory))

csvHolder = []
csvCounter = 0
for csvFile in os.listdir(flightLogDirectory):
    if csvFile[-3:].lower() == "csv":
        csvHolder.append(os.path.join(flightLogDirectory, csvFile))
        csvCounter = csvCounter + 1
print("Found %d CSV files in directory: %s" % (csvCounter, flightLogDirectory))

def howManySecs(clockFace):
    secs = int(clockFace[-2:]) + 60*int(clockFace[3:5]) + 60*60*int(clockFace[:2])
    return secs
        
with open(outputFilename, 'w') as outputFile:
    firstRow = "Image Name" + "," + "Time Taken" + "," + "Total Seconds" + "," + "Date Taken" + "\n"
    outputFile.write(firstRow)
    exifSecs = []
    for i in range(jpgCounter):
        image = Image.open(fileHolder[i])
        info = image._getexif()
        string = "DateTimeOriginal"
        for tag, value in info.items(): 
            key = TAGS.get(tag, tag)
            #print(key + " " + str(value))  #Would print out all exif data
            if key == string:
                row = fileHolder[i] + "," + str(value[-8:]) + "," + str(howManySecs(value[-8:])-offsetSecs) + "," + str(value[0:10]) + "\n"
                exifSecs.append(howManySecs(value[-8:]))
                outputFile.write(row)

image.close()
print("Output csv file for jpg image times created at location:", outputFilename)

flightImageSummary = []
for flight in range(csvCounter):

    with open(csvHolder[flight]) as flightFile:      
        flightFileLines = flightFile.read().split("\n")
    
    camShotLine = []
    word = 'SUCCESSED SIMPLE_SHOT'
    
    for i,line in enumerate(flightFileLines):
        if word in line: # or word in line.split() to search for full words
            camShotLine.append(i)
    
    missionRangeLine = []
    missStartLine = 0
    
    while(missStartLine == 0):
        for missionSpeed in range(2, 10):
            startWord = '[L-MIS]WP Mission: received idle vel cmd ' + str(missionSpeed)       
            for i,line in enumerate(flightFileLines):
                if startWord in line: # or word in line.split() to search for full words
                    missionRangeLine.append(i)
                    print("Word \"{}\" found in line {}".format(startWord, i))
                    missStartLine = i
                         
    endWord = 'turn mode. end of trace. quit'
    
    for j,line in enumerate(flightFileLines):
        if endWord in line: # or word in line.split() to search for full words
            missionRangeLine.append(j)
            missEndLine = j
            print("Word \"{}\" found in line {}".format(endWord, j))
    
    potMatch = len(camShotLine)
    potMatchLines = [flightFileLines[x] for x in camShotLine]
    
    dateWord = '|#SiF%|2'
    
    times = []
    flightTimes = []
    
    for y in range(potMatch):
        if potMatchLines[y].find(dateWord):
            times.append(potMatchLines[y][(potMatchLines[y].find(dateWord)+16):((potMatchLines[y].find(dateWord)+24))])
            flightTimes.append((flightFileLines[camShotLine[y]]).split(',')[1])
    
    #offsetTime from the flight file for mission start and end
    missStartFlightTime = (flightFileLines[missStartLine]).split(',')[1]
    missFinishFlightTime = (flightFileLines[missEndLine]).split(',')[1]
    #Difference between that and the offsetTime for the file line which we have the GPS time for
    flightTimeDiffs = [float(missStartFlightTime)-float(flightTimes[0]), float(missFinishFlightTime)-float(flightTimes[0])]
    
    #This calculates the real time for mission start and end, in format HH:MM:SS
    realFlightTimes = [0,0]
    for j in range(2):
        timeHolder = (times[0]).split(':')
        for i in range(3):
            timeHolder[i] = float(timeHolder[i])
        timeHolder[2] = timeHolder[2] + flightTimeDiffs[j]
        while timeHolder[2] >= 60:
            timeHolder[2] = timeHolder[2] - 60
            timeHolder[1] = timeHolder[1] + 1
            while timeHolder[1] >= 60:
                timeHolder[1] = timeHolder[1] - 60
                timeHolder[0] = timeHolder[0] + 1
        while timeHolder[2] <= 0:
            timeHolder[2] = timeHolder[2] + 60
            timeHolder[1] = timeHolder[1] - 1
            while timeHolder[1] <= 0:
                timeHolder[1] = timeHolder[1] + 60
                timeHolder[0] = timeHolder[0] - 1
        realFlightTimes[j] = timeHolder
    
    #Information required from the flight file
    offsetTimes = [(flightFileLines[x]).split(',')[1] for x in range(1, len(flightFileLines)-1)]
    longitudes = [(flightFileLines[x]).split(',')[3] for x in range(1, len(flightFileLines)-1)]
    latitudes = [(flightFileLines[x]).split(',')[4] for x in range(1, len(flightFileLines)-1)]
    altitudes = [(flightFileLines[x]).split(',')[10] for x in range(1, len(flightFileLines)-1)]
    
    #Calculates the number of seconds in a day since the start and end of the flight
    startSecond = 60*60*realFlightTimes[0][0] + 60*realFlightTimes[0][1] + realFlightTimes[0][2]
    endSecond = 60*60*realFlightTimes[1][0] + 60*realFlightTimes[1][1] + realFlightTimes[1][2]
    #In seconds elapsed during the day
    zerothRealTime = startSecond - (float(offsetTimes[missStartLine-1]) - float(offsetTimes[0]))
    
    with open(directory+'Flight'+str(flight+1)+'SummaryFlightFile.csv', 'w') as outputFlightFile:
        flightInSeconds = []
        firstRow = "Mission Start Line" + "," + str(missStartLine) + "," + "Mission End Line" + "," + str(missEndLine) + "\n"
        outputFlightFile.write(firstRow)
        secondRow = "Seconds" + "," + "Longitude" + "," + "Latitude" + "," + "Altitude" + "\n"
        outputFlightFile.write(secondRow)
        for i in range(0, len(flightFileLines)-2):  #I took out the +/- 20 buffer here, maybe erroneously
            timeInSeconds = float(offsetTimes[i]) - float(offsetTimes[0]) + zerothRealTime
            flightInSeconds.append(str(timeInSeconds))
            row =  str(timeInSeconds) + "," + longitudes[i] + "," + latitudes[i] + "," + altitudes[i] + "\n"
            outputFlightFile.write(row)
    
    print("Summary Flight File successfully written at location:", directory+'Flight'+str(flight+1)+'SummaryFlightFile.csv')
    
    #Code block for calculating the offset between GPS and Exif times
    
    successedInSecs = [flightInSeconds[x] for x in camShotLine]
    matches = []
    camShotMasterHolder = []
    camShotHolder = []
    exifHolder = []
    for i in range(len(exifSecs)):
        exifHolder.append(exifSecs[i])
    offsetRange = 4000
    
    for i in range(len(exifSecs)):
        exifHolder[i] = exifHolder[i] - offsetRange
        
    for i in range(offsetRange*2):
        matchCnt = 0
        camShotHolder = []
        if i%(2*offsetRange/10) == 0 and i != 0:
                print("Time offset calculator is %d per cent complete" % int((100*float(i))/(2*offsetRange)))
        for j in range(len(exifSecs)):
            exifHolder[j] = exifHolder[j] + 1
            for k in range(len(successedInSecs)):
                if successedInSecs[k].find(str(exifHolder[j]-2)) != -1:
                    matchCnt = matchCnt + 1
                    camShotHolder.append(k)
                    break
                if successedInSecs[k].find(str(exifHolder[j]-1)) != -1:
                    matchCnt = matchCnt + 1
                    camShotHolder.append(k)
                    break
                if successedInSecs[k].find(str(exifHolder[j])) != -1:
                    matchCnt = matchCnt + 1
                    camShotHolder.append(k)
                    break
                if successedInSecs[k].find(str(exifHolder[j]+1)) != -1:
                    matchCnt = matchCnt + 1
                    camShotHolder.append(k)
                    break
                if successedInSecs[k].find(str(exifHolder[j]-2)) != -1:
                    matchCnt = matchCnt + 1
                    camShotHolder.append(k)
                    break
        matches.append(matchCnt)
        camShotMasterHolder.append(camShotHolder)
                
    #print("Matched %d JPGs to the flight file with their corresponding line number listed below:" % (cnt3-cnt2))
    #print(jpgSecondsLineNum) 
    print(matches)
    print(min(matches), max(matches))
    indices = [i for i, x in enumerate(matches) if x == max(matches)]
    print(indices)
    trueOffset = int((max(indices)+min(indices))/2)
    
    if trueOffset < offsetRange:
        diffWord = 'ahead'
    elif trueOffset > offsetRange:
        diffWord = 'behind'
    else:
        diffWord = 'different'
    
    print("The exif image times are %d seconds %s of the onboard GPS time" % (abs(offsetRange-trueOffset), diffWord))
    
    with open(directory+'Flight'+str(flight+1)+'SummaryFlightFile.csv', 'r') as inputFlightFile:
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
    
#    cnt = 0
#    jpgSecondsLineNum = []
#    
#    #This for loop will compare the jpg exif times in seconds with that of the
#    #mission times in seconds, if there are matches it
#    #Will find 46 in 746 btw so be carfeul!!!!!
#    cnt2 = 0
#    cnt3 = 0
#    for sec in jpgSeconds:
#        cnt = 0
#        cnt3 = cnt3 + 1
#        while cnt==0:
#            try:
#                jpgSecondsLineNum.append(intMissionSeconds.index(sec))
#                break
#            except ValueError:
#                cnt = cnt + 1
#                cnt2 = cnt2 + 1
#                jpgSecondsLineNum.append(0)            
#    
#    print("Matched %d JPGs to the flight file with their corresponding line number listed below:" % (cnt3-cnt2))
#    print(jpgSecondsLineNum) 
    
    #Creates csv file for the data of images on Mission for the flight    
    with open(directory+'Flight'+str(flight+1)+'FinalMissionData.csv', 'w') as jpgFinalDataFile:
        firstRow = "File Name" + "," + "Longitude" + "," + "Latitude" + "," + "Altitude" + "\n"
        jpgFinalDataFile.write(firstRow)
        for i in range(max(matches)):
            lineNum = camShotLine[camShotMasterHolder[trueOffset][i]]
            row = jpgImageNames[i] + "," + longitudes[lineNum] + "," + latitudes[lineNum] + "," + altitudes[lineNum] + "\n"
            jpgFinalDataFile.write(row)
    
    print("Written CSV file of images from this flight and on mission to location:", directory+'Flight'+str(flight+1)+'FinalMissionData.csv')
                
#    ##Creates csv file for the names of images not on Mission for the flight 
#    with open(directory+'Flight'+str(flight+1)+'FinalNotMissionData.csv', 'w') as jpgFinalDataFile:
#        firstRow = "File Name" + "\n"
#        jpgFinalDataFile.write(firstRow)
#        for i in range(len(jpgSeconds)):
#            lineNum = jpgSecondsLineNum[i]
#            if lineNum != 0:
#                if lineNum <= missStartLine or lineNum >= missEndLine:
#                    row = jpgImageNames[i] + "\n"
#                    jpgFinalDataFile.write(row)
#            if type(lineNum) != int and type(lineNum) != float:
#                row = jpgImageNames[i] + "\n"
#                jpgFinalDataFile.write(row)
#                
#    print("Written CSV file of images from this flight but not on mission to location:", directory+'Flight'+str(flight+1)+'FinalNotMissionData.csv')
#    
    #Creates the new folders for JPGs and ARWs that are in and not in the mission        
    newpath1 = directory + 'Flight'+str(flight+1)+ 'MissionData/jpg/'  
    #newpath2 = directory + 'Flight'+str(flight+1)+ 'NotMissionData/jpg/'
    newpath3 = directory + 'Flight'+str(flight+1)+ 'MissionData/arw/'  
    #newpath4 = directory + 'Flight'+str(flight+1)+ 'NotMissionData/arw/' 
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
    #if not os.path.exists(newpath2):
        #os.makedirs(newpath2)
    if not os.path.exists(newpath3):
        os.makedirs(newpath3)
    #if not os.path.exists(newpath4):
        #os.makedirs(newpath4)
    
    #Reads in the csv with the final mission data for that flight and moves
    #the corresponding ARW/JPGs to the MissionData folder        
    with open(directory+'Flight'+str(flight+1)+'FinalMissionData.csv', 'r') as jpgFinalDataFile:
        jpgLines = jpgFinalDataFile.read().split("\n")
        missionImagesMoved = 0
        if len(jpgLines) > 2:
            jpgImageNames = [(jpgLines[x]).split(',')[0] for x in range(1, len(jpgLines)-1)]
            arwImageNames = [name[:-3] + "ARW" for name in jpgImageNames]   
            tempImage = (jpgImageNames[0]).split('/')
            fileLocal = len(tempImage)
            jpgImageFileNames = [(jpgImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
            arwImageFileNames = [(arwImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
            missionImagesMoved = len(jpgImageNames)
            for i in range(len(jpgImageNames)):
                os.rename(jpgImageNames[i],  newpath1 + jpgImageFileNames[i])
                os.rename(arwImageNames[i],  newpath3 + arwImageFileNames[i])
                if i%5 == 0 and i != 0:
                    print("Moved ARW and JPG %d out of %d to their MissionData folder" % (i, len(jpgImageNames)))
    
    flightImageSummary.append(missionImagesMoved)
    print("Moved JPG and ARW images that were in this flight and on the mission to their corresponding mission data folder")
    
#    #Reads in the csv with the final not mission data for that flight and moves
#    #the corresponding ARW/JPGs to the NotMissionData folder 
#    with open(directory+'Flight'+str(flight+1)+'FinalNotMissionData.csv', 'r') as jpgFinalDataFile:
#        jpgLines = jpgFinalDataFile.read().split("\n")
#        notmissionImagesMoved = 0
#        if len(jpgLines) > 2:
#            jpgImageNames = [(jpgLines[x]).split(',')[0] for x in range(1, len(jpgLines)-1)]
#            arwImageNames = [name[:-3] + "ARW" for name in jpgImageNames]
#            tempImage = (jpgImageNames[0]).split('/')
#            fileLocal = len(tempImage)
#            jpgImageFileNames = [(jpgImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
#            arwImageFileNames = [(arwImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
#            notmissionImagesMoved = len(jpgImageNames)
#            for i in range(len(jpgImageNames)):
#                os.rename(jpgImageNames[i],  newpath2 + jpgImageFileNames[i])
#                os.rename(arwImageNames[i],  newpath4 + arwImageFileNames[i])
#                if i%5 == 0:
#                    print("Moved ARW and JPG %d out of %d to their NotMissionData folder" % (i, len(jpgImageNames)))
#    
#    flightImageSummary.append(notmissionImagesMoved)        
#    print("Moved JPG and ARW images that were in this flight but not on the mission to their corresponding not mission data folder")

#Now create a txt file containing a summary of how many images are in each
#flight, useful for when there images taken during a flight but no images
#taken on mission        
with open(directory+'FinalFlightSummary.txt', 'w') as flightSummary:
     for i in range(csvCounter):
         row = "Flight Number" + "\t" + str(i+1) + "\t" + "In Mission ARW/JPG" + "\t" + str(flightImageSummary[i*2]) +  "\n" #"\t" + "Not In Mission ARW/JPG" + "\t" + str(flightImageSummary[i*2+1]) + "\n"
         flightSummary.write(row)
    
print("Written summary of the day's flights at location:", directory+'FinalFlightSummary.txt')
        
print('\a')
print("All done :)")