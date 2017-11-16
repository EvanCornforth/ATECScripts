import os

main_path = 'C:/Users/Evan/Documents/PhD/DCIM/testDCRAW'

pathBits = main_path.split('/')

if len(pathBits[-1]) == 0:
    main_path = main_path[:-2]

pathBits[-1] = "tiff"
fullPath = ''
for i in range(len(pathBits)):
        fullPath = fullPath + pathBits[i] + "/" 

if not os.path.exists(fullPath):
    os.makedirs(fullPath)
    print("Made new folder for the .tiff images at: ", fullPath)
 
tiffFileHolder = []
tiffPathHolder = []
tiffCounter = 0   
for file in os.listdir(main_path):
    if file.endswith(".tiff"):
        tiffPathHolder.append(os.path.join(main_path, file))
        tiffFileHolder.append(file)
        tiffCounter = tiffCounter + 1
        
for j in range(tiffCounter):
        os.rename(tiffPathHolder[j],  fullPath + tiffFileHolder[j])
        
print("Moved %d .tiff files to new folder from the folder %s" % (tiffCounter, main_path))
