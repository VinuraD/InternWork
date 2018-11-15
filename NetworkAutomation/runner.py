#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#		*-----------------*		  #
#		 Vinura Dhananjaya        #
#		*-----------------*		  #	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import absolute_import,division,print_function  #needed in python2 to execute some python3 commands
import netmiko													#handles SSH connections
import json														#handles format 
import os														#needed to build new directories etc.
import sys														#needed to read arguements from the command line
import tools													#custom library
import signal 													#handles keyboard interrupts and IOErrors

#connection = netmiko.ConnectHandler(ip= ip_address, device_type = cisco_ios, username = username, password = password)

# signal.signal(signal.SIGPIPE, signal.SIG_DFL)
# signal.signal(signal.SIGINT, signal.SIG_DFL)

if len(sys.argv)<3:
	print("Usage: runner.py commands.txt devices.json")
	exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = tools.get_credentials()

with open(sys.argv[1]) as commands_file:
	commands = commands_file.readlines()
	
with open(sys.argv[2]) as devices_file:
	devices = json.load(devices_file) 							#json format is pretty much similar to the python's dictionary format

for device in devices:
	device['username'] = username
	device['password'] = password
	try:
		print('='*79)											#PEP8 style
		print('Connecting to the device: ' + device['ip'])
		connection = netmiko.ConnectHandler(**device)
		newdir = connection.base_prompt
		filename = connection.base_prompt + '.txt'
		try:
			os.mkdir(newdir)
		except OSError as error:
			if error.errno == 17:
				print('Directory', newdir, 'already exists.')
			else:
                # re-raise the exception if some other error occurred.
				raise
			
		for command in commands:
			filename = command.rstrip().replace(' ', '_') + '.txt'
			filename = os.path.join(newdir, filename)
			with open(filename,'w') as outputfile:	
				print("Output of "+ command)
				print(connection.send_command(command))
				print()											#prints a newline
				outputfile.write(connection.send_command(command) + '\n\n')
				outputfile.write('='*79 + '\n\n')
		connection.disconnect()
		
	except netmiko_exceptions as exception:
		print('Failed to '+ device['ip']+str(exception)) ####*****************####
	
	except TimeoutError:
		print('Failed to '+ device['ip']+str(exception))




