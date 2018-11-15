#!usr/bin/env python
import os
import shutil
import glob
#can be done also using os.environ/threading/subprocess etc
def filebuff():
	f = open('track.txt','r') 
	time = float(f.readlines()[0])
	list_of_files = glob.glob(r'C:\CDRLogs\*')
	tbr = []
	for file in reversed(list_of_files):
		if time<os.path.getctime(file):
			tbr.append(file)
		else:
			break
	
	time=os.path.getctime(tbr[-1])
	f.close()
	f = open('track.txt','w+')
	f.write(str(time))
	f.close()

	return tbr
			
#at the start check for new logs,prev. pointer saved on txt file.work on them
	
		
		
