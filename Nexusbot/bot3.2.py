
###################################
# Source:webex.developers.com     #
# Edited and Developed by: VinuraD#
# 2018.11.20                      #
###################################
from itty import *
import urllib2
import json
import subprocess
import random
import re
from cli import *

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
	
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    #cont = ssl._create_unverified_context()
    contents = urllib2.urlopen(request).read()
    return contents
    
def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
	
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    #cont = ssl._create_unverified_context()
    contents = urllib2.urlopen(request).read()
    return contents
    

@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken.
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        try:
            if 'Hi' in in_message or 'hi' in in_message:
                msg = random.choice(["Hello!human","Hi","Hello there","Hello!Greetings from machine"])+", "+str((webhook['data']['personEmail'].split('@'))[0])
            elif 'who' in in_message or 'your' in in_message:
                msg = "I'm the NexusBot"
            elif 'cpu' in in_message:            
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'Sure!Will do!'})
                p = subprocess.Popen(["dohost","show processes cpu"],stdout=subprocess.PIPE)
                output,error = p.communicate()
                index = re.search(r'\b(CPU util)\b', output)
                msg = output[index.start():].rstrip()
            elif 'core' in in_message:
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'Sure!Will do!'})
                p = subprocess.Popen(["dohost","show cores"],stdout=subprocess.PIPE)
                output,error = p.communicate()
                msg = output
            elif 'shut' in in_message or 'off' in in_message:
                if len(re.findall(r'\d+',in_message))<2:
                       sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'What is the interface you want to shutdown!'})
                else:
                       intrf = 'interface eth'+re.findall(r'\d+',in_message)[0]+'/'+re.findall(r'\d+',in_message)[1]
                       subprocess.call(["dohost","conf t ; "+intrf+" ; shut"])
                       sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'Done!'})
            elif 'up' in in_message or ('no' in in_message and 'shut' in in_message):
                if len(re.findall(r'\d+',in_message))<2:
                       sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'What is the interface you want to turn up!'})
                else:
                       intrf = 'interface eth'+re.findall(r'\d+',in_message)[0]+'/'+re.findall(r'\d+',in_message)[1]
                       subprocess.call(["dohost","conf t ; "+intrf+" ; no shut"])
                       sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'Done!'})
                       
            else:
                msg = random.choice(["I am afraid I cannot answer that","Please ask me something else","I am sorry!I do not know answer for that one","Oops!I have no idea"])
            if msg != None:
                print msg
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
        except:
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": 'Oops,Something went wrong!'})
                                              
    return "true"

####CHANGE THESE VALUES#####
bot_email = "nexusbot@webex.bot"
bot_name = "NexusBot"
bearer = "Token"
run_itty(server='wsgiref', host='ip', port=10010)
