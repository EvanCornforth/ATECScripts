# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:24:25 2017

@author: Evan
"""

#compatibility PhotoScan Professional 1.3.0

import os

directoryInput = input('Enter the directory of the CSV files: ')
main_path = directoryInput.replace("\\", "/")

WIDTH = 640 #640
HEIGHT = 480 #512
DELIMITER = ";" #","
ABS_MAX = 65535
ABS_MIN = 0

files = os.listdir(main_path)
thermal = list()
min_t, max_t = 10.0E+10, 10.0E-10

#finding min and max
for file in files:

	if file[-3:].lower() != "csv":
		continue
	file_csv = open(main_path + "/" + file, "rt")
	for y in range(HEIGHT):
		line = file_csv.readline()
		pixels = [float(x) for x in line.strip().split(DELIMITER) if x]
		max_t = max(max(pixels), max_t)
		min_t = min(min(pixels), min_t)
	file_csv.close()

print("Maximum temperature is: %d and Minimum temperature is: %d" % (max_t, min_t))

print("script finished")