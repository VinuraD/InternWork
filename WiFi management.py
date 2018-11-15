#-------------------------------------------------------------------------------
# Name:        redServer
# Purpose:
#
# Author:      aadhilm
# Edited:      yohann,vinurad
# Created:     06/10/2014
# Copyright:   (c) aadhilm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket
import select
#import config as cfg
import Queue
import threading
import thread
import sys
from random import randint
from time import sleep
from ftplib import FTP
import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from datetime import datetime

class redFTP(threading.Thread):
    def __init__(self):
        super(redFTP,self).__init__()
        self.runing = True

    def read_ftp(self, c):
        try:
            ftp = FTP(host='ip',user='user',passwd='pass')
            #ftp = FTP(host='127.0.0.1',user='user',passwd='pass')
            ftp.cwd("/WiFi")

            files = ftp.nlst()
            print files

            for index in range(len(files)):
                print 'Current File is :', files[index]
                localfile = open((files[index]), 'wb')

                filex = ftp.retrbinary('RETR ' + files[index],localfile.write)
                localfile.close()

                print localfile
                print filex

                try:
                    print "Entering 1"
                    DOMTree = xml.dom.minidom.parse(files[index])
                    collection = DOMTree.documentElement
                    type1 = collection.getElementsByTagName('TRTY')[0]
                    if type1.childNodes[0].data=='CO':
                        nowTime = datetime.now()
                        fileTime = ftp.sendcmd('MDTM '+files[index])
                        fileTime = datetime.strptime(fileTime[4:], "%Y%m%d%H%M%S")
                        timelag = abs(fileTime-nowTime)
                        
                        timelogs = open("COLogs", "a")
                        timelogs.write("CO file : " + files[index] + " created at " + str(fileTime) + " where system time is " + str(nowTime) + "\n")
                        timelogs.close()

                        if timelag.seconds < 10800:
                            f.processXml(collection, c)
                            ftp.delete(files[index])
                        else:
                            pass
                    else:
                        f.processXml(collection, c)
                        ftp.delete(files[index])
                                
                except:
                    logfile = open("xmlERROR", "a")
                    logfile.write("there was an xml error " + files[index] +" at " + time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
                    logfile.close()
                    #ftp.delete(files[index])

                logfileproc = open("XMLProc", "a")
                logfileproc.write("XML Processes " + files[index] + time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
                logfileproc.close()

        except:
                logfile = open("ftpERROR", "a")
                logfile.write("there was an FTP server error at "+ time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
                logfile.close()
                return
				

        

    def processXml(self,collection, c):
        #collection = DOMTree.documentElement
        print "processing xml"
        type = collection.getElementsByTagName('TRTY')[0]
        print type.childNodes[0].data

        if type.childNodes[0].data == 'CI':
            f.checkINEvent(collection, c)
        if type.childNodes[0].data == 'NC':
            f.checkINEvent(collection, c)
        if type.childNodes[0].data == 'CO':
            f.checkOUTEvent(collection, c)
        if type.childNodes[0].data == 'RC':
            f.roomChange(collection, c)


    def checkINEvent(self,collection, c):
        print 'this is a checkin event'
        type = collection.getElementsByTagName('TRTY')[0]
        print 'the evernt type is' + type.childNodes[0].data

        type = collection.getElementsByTagName('HOTE')[0]
        hotelID = type.childNodes[0].data
        #print 'the hotel is' + type.childNodes[0].data

        type = collection.getElementsByTagName('ROOM')[0]
        roomID = type.childNodes[0].data

        try:

            if collection.getElementsByTagName('LNAM') and collection.getElementsByTagName('LNAM')[0].childNodes[0].data.lower() != 'na':
                checkstring = collection.getElementsByTagName('LNAM')
                print checkstring
                print 'this is true'
                type = collection.getElementsByTagName('LNAM')[0]
                fullName = type.childNodes[0].data
                nameList = fullName.split(' ')
                lastName = nameList[len(nameList)-1]
             
            else:
                type = collection.getElementsByTagName('FNAM')[0]
                fullName = type.childNodes[0].data
                nameList = fullName.split(' ')
                lastName = nameList[len(nameList)-1]
               
        except:
            type = collection.getElementsByTagName('FNAM')[0]
            fullName = type.childNodes[0].data
            nameList = fullName.split(' ')
            lastName = nameList[len(nameList)-1]
                 
        type = collection.getElementsByTagName('RESID')[0]
        reservationNo = type.childNodes[0].data

        preCheckIn = "GI|RN"+roomID+"|G#"+roomID+"|GSN|GNred"+roomID+"|"
        checkOutMessage = "GO|RN"+roomID+"|G#"+roomID+"|GSN|"
        checkInMessage = "GI|RN"+roomID+"|G#"+roomID+"|GSN|GNred"+roomID+"|"
	
	#checkInMessage = "GI|RN"+roomID+"|GSN|GN"+lastName+"|"
        print checkOutMessage
        
        print checkInMessage

        #c.send(preCheckIn)
        c.send(checkOutMessage)
        time.sleep(5)
        c.send(checkInMessage)
        time.sleep(5)
        c.send(checkOutMessage)
        time.sleep(5)
        c.send(checkInMessage)
        logfile = open("checkIN", "a")
        logfile.write(checkInMessage + time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
        logfile.close()

    def roomChange(self,collection, c):
        print 'this is a room change event'
        type = collection.getElementsByTagName('TRTY')[0]
        print 'the evernt type is' + type.childNodes[0].data

        type = collection.getElementsByTagName('HOTE')[0]
        hotelID = type.childNodes[0].data
        #print 'the hotel is' + type.childNodes[0].data

        type = collection.getElementsByTagName('OROOM')[0]
        roomID = type.childNodes[0].data

        try:

            if collection.getElementsByTagName('LNAM') and collection.getElementsByTagName('LNAM')[0].childNodes[0].data.lower() != 'na':
                checkstring = collection.getElementsByTagName('LNAM')
                print checkstring
                print 'this is true'
                type = collection.getElementsByTagName('LNAM')[0]
                fullName = type.childNodes[0].data
                nameList = fullName.split(' ')
                lastName = nameList[len(nameList)-1]
             
            else:
                type = collection.getElementsByTagName('FNAM')[0]
                fullName = type.childNodes[0].data
                nameList = fullName.split(' ')
                lastName = nameList[len(nameList)-1]
               
        except:
            type = collection.getElementsByTagName('FNAM')[0]
            fullName = type.childNodes[0].data
            nameList = fullName.split(' ')
            lastName = nameList[len(nameList)-1]
                 
        #type = collection.getElementsByTagName('RESID')[0]
        #reservationNo = type.childNodes[0].data

        preCheckIn = "GI|RN"+roomID+"|G#"+roomID+"|GSN|GNred"+roomID+"|"
        checkOutMessage = "GO|RN"+roomID+"|G#"+roomID+"|GSN|"
        checkInMessage = "GI|RN"+roomID+"|G#"+roomID+"|GSN|GNred"+roomID+"|"
	
	#checkInMessage = "GI|RN"+roomID+"|GSN|GN"+lastName+"|"
        print checkOutMessage
        
        print checkInMessage

        #c.send(preCheckIn)
        c.send(checkOutMessage)
        time.sleep(5)
        c.send(checkInMessage)
        time.sleep(5)
        c.send(checkOutMessage)
        time.sleep(5)
        c.send(checkInMessage)
        
        logfile = open("roomChange", "a")
        logfile.write(checkInMessage + time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
        logfile.close()


    def checkOUTEvent(self,collection, c):
        print 'this is a checkout event'
        type = collection.getElementsByTagName('TRTY')[0]
        print 'the evernt type is' + type.childNodes[0].data

        type = collection.getElementsByTagName('HOTE')[0]
        hotelID = type.childNodes[0].data
        #print 'the hotel is' + type.childNodes[0].data

        type = collection.getElementsByTagName('ROOM')[0]
        roomID = type.childNodes[0].data

        if collection.getElementsByTagName('LNAM'):
            type = collection.getElementsByTagName('LNAM')[0]
            fullName = type.childNodes[0].data
            nameList = fullName.split(' ')
            lastName = nameList[len(nameList)-1]
        else:
            type = collection.getElementsByTagName('FNAM')[0]
            fullName = type.childNodes[0].data
            nameList = fullName.split(' ')
            lastName = nameList[len(nameList)-1]


        type = collection.getElementsByTagName('RESID')[0]
        reservationNo = type.childNodes[0].data


        #checkOutMessage = "GO|RN"+roomID+"|G#"+reservationNo+"|GSN|"
        checkOutMessage = "GO|RN"+roomID+"|G#"+roomID+"|GSN|"

        logfile = open("checkOUT", "a")
        logfile.write(checkOutMessage + time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") + "\n")
        logfile.close()
        
        print checkOutMessage
        c.send(checkOutMessage)
        time.sleep(5)

class send_message(threading.Thread):
    def __init__(self):
        super(send_message,self).__init__()
        self.runing = True
        self.q = Queue.Queue()

    def send(self,data,connection):
        connection.send(data)


class receive_message(threading.Thread):
    def __init__(self):
        super(receive_message,self).__init__()
        self.runing = True


    def receive(self,c):
        #while True:
            print('.')
            ready = select.select([c,],[],[],2)

            if ready[0]:
                data = c.recv(2048)

                if data:
                    print data
                    c.send(data)
                #else:
                    #break

                if data[1] =="L" and data[2] =="A":
                    print "flag change to 1"
                    main.pmsFlag = 1
                    print "the pms flag now is"
                    print main.pmsFlag










t = receive_message()
t.start()

f = redFTP()
f.start()



port = 12346



def main():

    main.pmsFlag = 0


    redSocket=socket.socket()                                                   # Create socket object
    redSocket.bind(('ip',port))
    redSocket.listen(5)                                                          # Now wait for client connection.


    while 1:
        print 'Back to main 1 loop'
        redConnection, addr = redSocket.accept()                                 # Establish connection with client.
        print 'Got connection from', addr


        while 1:
            try:
                t.receive(redConnection)
                print"The PMS Flag is:"
                print main.pmsFlag

            except:
                main.pmsFlag = 0
                redConnection.close()
                logfileMainError = open("mainError", "a")
                logfileMainError.write("An Error Occured in the main loop "+ time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S") +"\n")
                logfileMainError.close()
				
                break

            
            if main.pmsFlag == 1:
                f.read_ftp(redConnection)





if __name__ == '__main__':
    main()
