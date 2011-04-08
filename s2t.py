import Skype4Py as sky
import time
import sys


chats_to_follow = ("The High Council of Disposia")
connected_to_skype = False

def attachment_status_change(status):
	global connected_to_skype

	print "API attachment status changed to: " + client.Convert.AttachmentStatusToText(status)
	if status == sky.apiAttachAvailable:
		connected_to_skype = False
		client.Attach();
	elif status == sky.apiAttachSuccess:
		print "successfully connected to skype"
		connected_to_skype = True
	
	elif status == sky.apiAttachUnknown:
		print "*************** unknown api attachment status *****************" 
		connected_to_skype = False
	elif status == sky.apiAttachPendingAuthorization:
		print "api authorization pending, please authorize this script in skype to listen to incoming messages"
		connected_to_skype = False
	elif status == sky.apiAttachRefused:
		print "api attachment refused, please authorize this script in skype to listen to incoming messages"
		connected_to_skype = False
	elif status == sky.apiAttachNotAvailable:
		print "no api hook available"
		connected_to_skype = False
			
def message_status_change(message, status):
	global chats_to_follow

	if str(message.Chat.Topic) in chats_to_follow:
		if status == 'RECEIVED' or status == 'SENT':
			print(message.FromDisplayName + ': ' + message.Body)
			##########message parsing code goes here##############
	

print "skype2tumblr started, initializing..."
client = sky.Skype()
client.OnAttachmentStatus = attachment_status_change;				# set event handler for api hook
client.OnMessageStatus = message_status_change;					# set event handler for message status

print "connecting to skype....."
client.Attach()									# connect to api hook
	
while not connected_to_skype:
	time.sleep(1)

while True:
	time.sleep(1)
