
directory = 'D:/ATEC/180717_sample/maia/20170718/'

import os
import re

folder_list = os.listdir(directory)

folder_list_count = len(folder_list)

for d in range(folder_list_count):
        text = folder_list[d]
        
        p = re.compile('Flight\dMissionData')
        
        folder = p.match(text)
    
        if folder:
            print text
        
        
        
        if fnmatch.fnmatch(text, 'Flight*MissionData'):
            print p.match
        
        data = re.search('Flight.MissionData',text)
        text.find = "Flight4MissionData":
            print 'yes'
#        if folder_list(d) == fnmatch.filter('Flight4MissionData'):
#            print('yes',d)
    

#count_mission_dir = 0
#
#folder_handler = os.listdir(directory)

