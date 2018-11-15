#!/usr/bin/env python
import os 
import time
import datetime
import shutil
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import subprocess
import socket
import sys



	
def checknew():
	fo = open('Position.txt','r')
	size = int(fo.readlines()[1].rstrip())
	fo.close()
	logsize = int(os.path.getsize("path"))
	if logsize==size:
		sys.exit()
	elif logsize<size:
		fo = open('Position.txt','w+')
		data=['0\n','0\n']
		fo.writelines(data)
		fo.close()
def command():
	#alarm = False
	error= ['Error,as,list,of,words']
	shutil.copy("path")
	fo=open('Position.txt','r')
	current = int(fo.readlines()[0].rstrip())
	fo.close()
	with open("/pythonscript/nohup.out") as file:
		file.seek(current)
		file_obj = file.readlines()
		current = file.tell()
		f = open('Position.txt','w+')	
		data=[str(current)+'\n',str(os.path.getsize("/pythonscript/nohup.out"))+'\n']
		f.writelines(data)
		f.close()
		###Try printing the read file contents.
		##print file_obj
	for strings in file_obj:
		list_log = strings.rstrip().split(' ')
		if len(frozenset(list_log).intersection(error))>=4:
			alarm = True
		else:
			alarm = False
	os.remove("/pythonscript/nohup.out")
	return alarm
	
# def check(logtext):
	# error= ['Time','Taken','For','TPE']#['TBMS','Server','Pause','Complete']
	# alarm = False
	# if len(frozenset(str(logtext).split()).intersection(error))>=4 :
		# alarm = True
	# return alarm	
		

#########################################################

def send_mail(send_from, send_to, subject, text, files=None, server="172.17.15.67", port= 25):
	msg = MIMEMultipart(From=send_from,To=send_to,Date=formatdate(localtime=True))
	msg['Subject']=subject
	msg.attach(MIMEText(text))            

	smtp = smtplib.SMTP(server, port)
	smtp.sendmail(send_from, send_to, msg.as_string())
	print('Mail sent')
	smtp.close()    
	    

	
###############################################################

if __name__=="__main__":
	checknew()
	flag = command()
	if flag == True:
		send_mail('mailserver','mymail',socket.gethostname(),'msg'+' '+'on'+' ' +str(time.ctime()))
		print('Success!')
	else:
		print('Normal')
		

				

	
	
