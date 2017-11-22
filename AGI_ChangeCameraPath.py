# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:09:20 2017

@author: Evan
"""

chunk1 = 0
chunk2 = 70
chunk3 = 120

chunk = PhotoScan.app.document.chunk
for i in range (len(chunk.cameras)):
    #if i >= chunk1 and i < chunk2:
    chunk.cameras[i].frames[0].path = chunk.cameras[i].path.replace("D:\WORKSHOP_DATA\WK_field\rgb", "D:\ATEC\Data\WK_field\rgb")
    #elif i >= chunk2 and i < chunk3:
    #    chunk.cameras[i].frames[0].path = chunk.cameras[i].path.replace(".jpg", ".tiff")
    #else:
    #    chunk.cameras[i].frames[0].path = chunk.cameras[i].path.replace(".jpg", ".tiff")
        
#chunk.cameras[0].frames[0].path = newpath.