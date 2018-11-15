#!usr/bin/env python
#########################################################
#                                                       #
#   Purpose:                                            #
#       Read logs and call APIs                         #
#                                                       #
#########################################################
#=======================================================#

import time
import csv
import os
import requests
import json
import sys
import glob
#========================================================#
import apicaller
import filehandler
import updatefile
#========================================================#

contents=updatefile.filebuff()



def find_index(file):
	fileobj = open(file)
	fileobj_read = csv.reader(fileobj,delimiter=',')
	for item in fileobj_read:
		index_no1 = item.index('finalCalledPartyNumber')
		index_no2 = item.index('callingPartyNumber')
		break
	fileobj.close()
	return index_no1,index_no2

#========================================================#	
	
def find_match(file,no1,no2):
	fileobj = open(file)
	fileobj_read = csv.reader(fileobj,delimiter=',')
	num = '512'#'117484555' 
	count = 0
	f = open('callingPartyNumbers.txt','w+') 
	#f.write(time.ctime()+'\n')
	#f.write('callingPartyNumbers'+'\n')
	for item in fileobj_read:
		if count == 0:
			count+=1
			#continue
		else:
			if num in str(item[no1]):
				out = (item[no2])
				f.write(out+'\n')
				print('logwrite!')
	fileobj.close()
	# if os.stat('callingPartyNumbers.txt').st_size == 0:
		# f.close()
		# sys.exit()
	# else:
		# f.close()
	f.close()
		
#========================================================#							

start_time = time.time()

# file_list=os.listdir()
# req_file = max(file_list,key=len)
for content in contents:
	filehandler.copyfile(content,r'C:\Script')#.format(filehandler.findfileorig()))	
	req_file = filehandler.findfile()
# files = glob.glob(r'C:\Script*')
# req_file = max(files,os.path.getctime)
	print(req_file)
	
	index1,index2=find_index(req_file)
	find_match(req_file,index1,index2)
#========================================================#

	
	with open('callingPartyNumbers.txt') as txtfile:#0 for test purpose 
		numbers=txtfile.readlines()

#========================================================#


	for number in numbers:
		if not(apicaller.API1(number)):
			if not(apicaller.API2(number)):
				apicaller.API4(number)
				print('called API4'+':'+number)
			else:
				p1,p2 = apicaller.API2(number)
				apicaller.API3(p1,p2)			
				print('called API3 from API1'+':'+number)
		else:
			p3,p4 = apicaller.API1(number)
			apicaller.API3(p3,p4)		
			print('called API3 from API1'+':'+number)

#========================================================#

	print('API calling took :'+str(round(time.time()-start_time))+' '+'seconds')

#========================================================#

	os.remove(req_file)

filehandler.buffer()
	
