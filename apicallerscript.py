#!usr/bin/env python
import requests
import json

def API1(innumbers):
	URL='api'.format(innumbers)#string formatting needed {}.format()
	headers = {'Authorization':'Basic token'}
	response = requests.get(URL,auth=('user,pass'))	
	if response.status_code != 200:
		print(response.status_code)
		# #raise ApiError('Error occured.Code: {}'.format(response.status_code))
		#return False
	else:
		output = response.json()
		#print(output)
		try:
			partyid = output['items'][0]['PartyId']#handle exception for KeyError
			contactname = output['items'][0]['ContactName']
			return partyid,contactname
		except KeyError:
			print('No matching Key')
			return False
	
	
		
		
def API2(innumbers):
	URL='api'.format(innumbers)
	headers = {'Authorization':'Basic token'}
	response = requests.get(URL,auth=('user,pass'))
	if response.status_code != 200:
		print(response.status_code)
		#raise ApiError('Error occured.Code: {}'.format(response.status_code))
		#return False
	else:
		output = response.status_code
		try:
			partyid = output['items'][0]['PartyId']#handle exception for KeyError
			contactname = output['items'][0]['PrimaryContactName']
			return partyid,contactname
		except KeyError:
			print('No matching Key')
			return False
		
	
def API3(partyid,contactname):
	URL='api'
	
	payload = {"ActivityFunctionCode" : "TASK","Subject" : "Test2",
	"AccountId": 300000001917986,"ActivityTypeCode":"CALL","ActivityPartialDescription":"Testing",
	"CallStatus_c": "OFF"}
	payload['AccountId'] = partyid
	payload['Subject']='missed call from'+' '+contactname
	headers = {'Authorization':'Basic token'}
	
	response = requests.post(URL,json=payload,auth=('user,pass')) 
	
	if response.status_code != 201:
		print(response.status_code)
		#raise ApiError('Error occured.Code: {}'.format(response.status_code))
	else:
		output = response.json()
		print(response.status_code)
		
		
def API4(numberR):	
	URL='api'
	
	payload = {"ActivityFunctionCode" : "TASK","Subject" : "Test2","ActivityTypeCode":"CALL",
	"ActivityPartialDescription":"Testing","CallStatus_c": "OFF"}
	payload['Subject']='missed call from'+' '+numberR

	headers = {'Authorization':'Basic token'}
	
	response = requests.post(URL,json=payload,auth=('user,pass')) 
	
	if response.status_code != 201:
		print(response.status_code)
		#raise ApiError('Error occured.Code: {}'.format(response.status_code))
	else:
		output = response.json()
		print(response.status_code)