# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:40:14 2017

@author: Evan
"""

import os

path = 'C:/Users/Evan/Documents/PhD/DCIM/testDCRAW/'
arwCounter = 0   
for file in os.listdir(path):
    if file.endswith(".arw"):
        arwCounter = arwCounter + 1

os.system('C:\\Users\\Evan\\Documents\\PhD\\ATEC_Jupyter\\Convert_Dir_ARWTIFF.bat ' + path + " " + str(arwCounter))