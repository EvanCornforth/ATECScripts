# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:29:41 2017

@author: Evan
"""

import os

directoryInput = input('Enter the directory of JPG images: ')
directory = directoryInput.replace("\\", "/")

#Creates the new folders for JPGs and ARWs that are in and not in the mission        
newpath1 = directory + 'MissionData/jpg/'  
newpath2 = directory + 'NotMissionData/jpg/'
newpath3 = directory + 'MissionData/arw/'  
newpath4 = directory + 'NotMissionData/arw/' 
if not os.path.exists(newpath1):
    os.makedirs(newpath1)
if not os.path.exists(newpath2):
    os.makedirs(newpath2)
if not os.path.exists(newpath3):
    os.makedirs(newpath3)
if not os.path.exists(newpath4):
    os.makedirs(newpath4)
        
with open(directory+'/FinalMissionData.csv', 'r') as jpgFinalDataFile:
    jpgLines = jpgFinalDataFile.read().split("\n")
    jpgImageNames = [(jpgLines[x]).split(',')[0] for x in range(1, len(jpgLines)-1)]
    arwImageNames = [name[:-3] + "ARW" for name in jpgImageNames]   
    tempImage = (jpgImageNames[0]).split('/')
    fileLocal = len(tempImage)
    jpgImageFileNames = [(jpgImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
    arwImageFileNames = [(arwImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
    for i in range(len(jpgImageNames)):
        os.rename(jpgImageNames[i],  newpath1 + jpgImageFileNames[i])
        os.rename(arwImageNames[i],  newpath3 + arwImageFileNames[i])
 
print("Moved JPG and ARW images that were in this flight and on the mission to their corresponding mission data folder")
   
with open(directory+'/FinalNotMissionData.csv', 'r') as jpgFinalDataFile:
    jpgLines = jpgFinalDataFile.read().split("\n")
    jpgImageNames = [(jpgLines[x]).split(',')[0] for x in range(1, len(jpgLines)-1)]
    arwImageNames = [name[:-3] + "ARW" for name in jpgImageNames]
    tempImage = (jpgImageNames[0]).split('/')
    fileLocal = len(tempImage)
    jpgImageFileNames = [(jpgImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
    arwImageFileNames = [(arwImageNames[x]).split('/')[fileLocal-1] for x in range(len(jpgImageNames))]
    for i in range(len(jpgImageNames)):
        os.rename(jpgImageNames[i],  newpath2 + jpgImageFileNames[i])
        os.rename(arwImageNames[i],  newpath4 + arwImageFileNames[i]) 
        
print("Moved JPG and ARW images that were in this flight but not on the mission to their corresponding not mission data folder")
print("All done :)")