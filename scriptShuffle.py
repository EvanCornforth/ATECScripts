directory = 'C:/Users/Evan/Anaconda3/.ipynb_checkpoints/TestMover'

import os

fileHolder = []
fileCounter = 0
for file in os.listdir(directory):
    if file.endswith(".txt"):
        fileHolder.append(os.path.join(directory, file))
        fileCounter = fileCounter + 1

fileData = []

for i in range(fileCounter):
    newpath1 = directory + '/Flight' + str(i+1) + 'MissionData'  
    newpath2 = directory + '/Flight' + str(i+1) + 'NotMissionData'  
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
    if not os.path.exists(newpath2):
        os.makedirs(newpath2)
    with open(fileHolder[i]) as file:
        fileLines = file.read().split("\n")
        fileImageNames = [(fileLines[x]).split('\t')[3] for x in range(len(fileLines)-1)]
        fileAltitudes = [(fileLines[x]).split('\t')[12] for x in range(len(fileLines)-1)]
        missionAlts = []
        for k in range(1, len(fileAltitudes)):
            if float(fileAltitudes[k]) > 167 + 50:
                missionAlts.append(k)
        fileData.append((fileHolder[0], min(missionAlts), max(missionAlts)))
        for j in range(fileData[i][1], fileData[i][2]+1):
            os.rename(directory + '/' + fileImageNames[j],  newpath1 + '/' + fileImageNames[j])
        for a in range(1, fileData[i][1]):
            os.rename(directory + '/' + fileImageNames[a],  newpath2 + '/' + fileImageNames[a])
        for b in range(fileData[i][2]+1, len(fileImageNames)):
            os.rename(directory + '/' + fileImageNames[b],  newpath2 + '/' + fileImageNames[b])