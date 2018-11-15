#!usr/bin/env python
import os
import shutil
import glob

def findfile():
	file_list=os.listdir()
	reqfile = max(file_list,key=len)
	return reqfile
	
def buffer():
	if len(glob.glob(r'C:\CDRLogs\*'))>=100:
		for file in glob.glob(r'C:\CDRLogs\*'):
			os.remove(file)
	else:
		pass
def findfileorig():
	list_of_files = glob.glob(r'C:\CDRLogs\*')
	#print(list_of_files)
	latest = max(list_of_files,key=os.path.getctime)
	#print(latest)
	
	return latest
	
	
def copyfile(source,destination):
	#sourcefile = os.path.dirname(source)
	shutil.copy(source,destination)
	
	
	

	
		
		
