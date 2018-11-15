from __future__ import absolute_import,division,print_function

from getpass import getpass

def get_input(prompt=''):
	try:
		line = raw_input(prompt)
	except NameError:
		line = input(prompt)
	return line
	
def get_credentials():
	while True:
		username = get_input('Username: ')
		if len(str(username)):
			break
	password = None
	while not password:
		password = getpass('Password: ')
		pass_verify = getpass('Retype the password: ')
		if password!=pass_verify:
			print('Password mismatch')
			password = None
	return username, password