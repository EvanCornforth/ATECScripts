# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:24:25 2017

@author: Evan
"""

#compatibility PhotoScan Professional 1.3.0

import PhotoScan, os

main_path = PhotoScan.app.getExistingDirectory("Specify the folder with the CSV files:")

WIDTH = 640 #640
HEIGHT = 480 #512
DELIMITER = "," #","
ABS_MAX = 65535
ABS_MIN = 0

doc = PhotoScan.app.document
chunk = doc.addChunk()
chunk.label = "Chunk thermal"

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

#creating images	
for file in files:

	if file[-3:].lower() != "csv":
		continue
	
	file_csv = open(main_path + "/" + file, "rt")

	image = PhotoScan.Image(WIDTH, HEIGHT, " ", "U16")

	for y in range(HEIGHT):
		line = file_csv.readline()
		pixels = [float(x) for x in line.strip().split(DELIMITER) if x]
		for x in range(WIDTH):
			pixel = pixels[x] * (ABS_MAX - ABS_MIN) / (max_t - min_t)
			image[x,y] = (pixel,)
	file_csv.close()
			
	image.save(main_path + "/" + file[:-3] + "tif")	
	thermal.append(main_path + "/" + file[:-3] + "tif")
	
doc.chunk = chunk	
chunk.addPhotos(thermal)

print("script finished")