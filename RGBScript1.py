# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:13:46 2017

Takes in the corresponding flight file, and using the startWord = '[L-MIS]WP 
Mission: received idle vel cmd 2' or endWord = 'turn mode. end of trace. quit'
to associate the flight file lines with real times. Using this real time, the
total secodns past midnight is calculated. A new csv file is created, with
first line having the start and end line outputted, and then the next line
having column headers Seconds / Long / Lat / Altitude for every single line in
the flight file. This allows for later matching with image capture times that 
were on misson and not on mission.

@author: Evan
"""

flightLogDirectoryInput = input('Enter the flight log path: ')
flightLogDirectory = flightLogDirectoryInput.replace("\\", "/")

with open(flightLogDirectory) as flightFile:      
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

with open(directory+'/SummaryFlightFile.csv', 'w') as outputFlightFile:
    firstRow = "Mission Start Line" + "," + str(missStartLine) + "," + "Mission End Line" + "," + str(missEndLine) + "\n"
    outputFlightFile.write(firstRow)
    secondRow = "Seconds" + "," + "Longitude" + "," + "Latitude" + "," + "Altitude" + "\n"
    outputFlightFile.write(secondRow)
    for i in range(0, len(flightFileLines)-2):  #I took out the +/- 20 buffer here, maybe erroneously
        timeInSeconds = float(offsetTimes[i]) - float(offsetTimes[0]) + zerothRealTime
        row =  str(timeInSeconds) + "," + longitudes[i] + "," + latitudes[i] + "," + altitudes[i] + "\n"
        outputFlightFile.write(row)

print("Summary Flight File successfully written at location:", directory+'/SummaryFlightFile.csv')