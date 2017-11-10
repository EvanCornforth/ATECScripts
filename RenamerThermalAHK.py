#directoryInput = input('Enter the directory: ')
#directory = directoryInput.replace("\\", "/")
directory = 'C:/Users/arevill/Desktop/ATEC_data/THERMAL_PROCESSING/WK/fly0/'

offset = 0

import os

files = os.listdir(directory)
    
for file in files:
    if file[-3:].lower() == "csv":
        newFileNum = int(file[:-4]) + offset
        os.rename(directory + file,  directory + 'Flight1_' + str(newFileNum) + '.csv')
        
print("All done")