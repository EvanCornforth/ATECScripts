# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:20:55 2018
@author: evanc
"""

import os
from tkinter.filedialog import askdirectory

print("Please select the directory containing .Tiffs and .ARW images")
main_path = askdirectory()

pathBits = main_path.split('/')

if len(pathBits[-1]) == 0:
    main_path = main_path[:-2]

pathBits[-1] = "tiff"
fullPath = ''
for i in range(len(pathBits)):
        fullPath = fullPath + pathBits[i] + "\\" 

if not os.path.exists(fullPath):
    os.makedirs(fullPath)
    print("Made new folder for the .tiff images at:", fullPath)
 
tiffFileHolder = []
tiffPathHolder = []
tiffCounter = 0   
for file in os.listdir(main_path):
    if file[-4:].lower() == "tiff":
        tiffPathHolder.append(os.path.join(main_path, file))
        tiffFileHolder.append(file)
        tiffCounter = tiffCounter + 1
        
for j in range(tiffCounter):
        os.rename(tiffPathHolder[j], fullPath + tiffFileHolder[j])
        
print("Moved %d .tiff files to this new folder from %s" % (tiffCounter, main_path))