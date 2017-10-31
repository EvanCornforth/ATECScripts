directory = 'D:/ATEC/180717_sample/maia/20170718/Flight4MissionData/geom+stitch+radio+radial'

missionSpeed = 2
missionSpeedBumpiness = 0.5
missionAlt = 232
missionAltBumpiness = 3

import os

fileHolder = []
fileCounter = 0
for file in os.listdir(directory):
    if file.endswith(".log"):
        fileHolder.append(os.path.join(directory, file))
        fileCounter = fileCounter + 1

#print("Files are:", fileHolder)
#print("Number of files are:", fileCounter)

fileData = []

for i in range(fileCounter):
    newpath1 = directory + '/Flight' + str(i+1) + 'MissionData'  
    newpath2 = directory + '/Flight' + str(i+1) + 'NotMissionData'
    outputFileName = fileHolder[i][:-4] + 'MissionOnly.csv' 
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
   #     print("Made the folder:", newpath1)
    if not os.path.exists(newpath2):
        os.makedirs(newpath2)
   #     print("Made the folder:", newpath2)
    with open(fileHolder[i]) as file:
        fileLines = file.read().split("\n")
    #    print("First line is:", fileLines[0])
        fileImageNames = [(fileLines[x]).split('\t')[3] for x in range(len(fileLines)-1)]
        fileAltitudes = [(fileLines[x]).split('\t')[11] for x in range(len(fileLines)-1)]
        fileSpeeds = [(fileLines[x]).split('\t')[14] for x in range(len(fileLines)-1)]
        fileLongs = [(fileLines[x]).split('\t')[7] for x in range(len(fileLines)-1)]
        fileLats = [(fileLines[x]).split('\t')[9] for x in range(len(fileLines)-1)]
        missionAlts = []
        
        def speedChecker(vals, heightVals):
            cnt = 0
            for i in vals:
                if missionSpeed - missionSpeedBumpiness < i < missionSpeed + missionSpeedBumpiness:
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
            for i in vals:
                if missionAlt - missionAltBumpiness < i < missionAlt + missionAltBumpiness:
                    cnt = cnt + 1
            if cnt == len(vals):
                return 1
            else: 
                return 0
    
        check = 0
        counter = 1
        while check == 0:
            speedVals = [float(fileSpeeds[x]) for x in range(counter, counter+30)]
            heightVals = [float('0' + fileAltitudes[x]) for x in range(counter, counter+30)]
            counter = counter + 1
            check = speedChecker(speedVals, heightVals)
        missStartLine = counter
        print(missStartLine)

        check = 0
        counter = len(fileLines) - 1
        while check == 0:
            speedVals = [float(fileSpeeds[x]) for x in range(counter-30, counter)]
            heightVals = [float('0' + fileAltitudes[x]) for x in range(counter-30, counter)]
            counter = counter - 1
            check = speedChecker(speedVals, heightVals)
        missEndLine = counter
        print(missEndLine) 
        print('mission alts are', missionAlts)
        missionAlts = [c for c in range(missStartLine, missEndLine)]
        
        testMiss= []
        for k in range(1, len(fileAltitudes)):
            if float(fileAltitudes[k]) > 167 + 40:
                testMiss.append(k)
                
        testmissionStartLine = min(missionAlts)
        testmissionEndLine = max(missionAlts)
  
        fileData.append((fileHolder[i], missStartLine, missEndLine))
        newFileImageNames = [0 for x in range(len(fileLines)-1)]
        newFileImageNames[0] = fileImageNames[0]
        for a in range(1, len(fileLines)-1):
            newFileImageNames[a] = fileImageNames[a][:-3] + 'tif'
        if len(missionAlts) != 0:
            for j in range(fileData[i][1], fileData[i][2]+1):
                if fileLats[j] != '55.8905953333':
                    os.rename(directory + '/' + newFileImageNames[j],  newpath1 + '/' + newFileImageNames[j])  
       
        imageFileHolder = []
        file_name = []
        for file in os.listdir(directory):
            if file.endswith(".tif"):
                imageFileHolder.append(os.path.join(directory, file))  
        for im in range(len(imageFileHolder)):
            file_name.append(os.path.basename(imageFileHolder[im]))
            os.rename(directory + '/' + imageFileHolder[im][-30:], newpath2 + '/' + imageFileHolder[im][-30:])
      
        with open(outputFileName, 'w') as outputMaiaFile:
            firstRow = str(newFileImageNames[0]) + "," + str(fileLongs[0]) + "," + str(fileLats[0]) + "," + str(fileAltitudes[0]) + "\n"
            outputMaiaFile.write(firstRow)
            for d in range(missStartLine, missEndLine):
                if fileLats[d] != '55.8905953333':
                    row = newFileImageNames[d] + "," + '-' + fileLongs[d] + "," + fileLats[d] + "," + fileAltitudes[d] + "\n"
                    outputMaiaFile.write(row)