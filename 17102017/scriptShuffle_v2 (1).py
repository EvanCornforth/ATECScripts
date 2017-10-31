directory = 'D:/ATEC/180717_sample/maia/20170718'

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
        missionAlts = []
        for k in range(1, len(fileAltitudes)):
            if float(fileAltitudes[k]) > 167 + 50:
                missionAlts.append(k)
        if len(missionAlts) == 0:
            missionStartLine = 0
            missionEndLine = 0
        else:
            missionStartLine = min(missionAlts)
            missionEndLine = max(missionAlts)
 #       print("Sorted appropriate altitudes")
  #      print(fileAltitudes)
  #      print(fileImageNames) 
  #      print(missionAlts)
        fileData.append((fileHolder[i], missionStartLine, missionEndLine))
        if len(missionAlts) != 0:
            for j in range(fileData[i][1], fileData[i][2]+1):
                os.rename(directory + '/' + fileImageNames[j],  newpath1 + '/' + fileImageNames[j])
        for a in range(1, fileData[i][1]):
            os.rename(directory + '/' + fileImageNames[a],  newpath2 + '/' + fileImageNames[a])
        for b in range(fileData[i][2]+1, len(fileImageNames)):
            os.rename(directory + '/' + fileImageNames[b],  newpath2 + '/' + fileImageNames[b])    