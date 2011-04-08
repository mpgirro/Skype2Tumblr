import Skype4Py as sky
import time
import sys


chats_to_follow = ("The High Council of Disposia")

def attachment_status_change(status):

	print "API attachment status changed to: " + client.Convert.AttachmentStatusToText(status)
	if status == sky.apiAttachAvailable:
		client.Attach();
	elif status == sky.apiAttachSuccess:
		print "successfully connected to skype"
	
	elif status == sky.apiAttachUnknown:
		print "*************** unknown api attachment status *****************" 
	elif status == sky.apiAttachPendingAuthorization:
		print "api authorization pending, please authorize this script in skype to listen to incoming messages"
	elif status == sky.apiAttachRefused:
		print "api attachment refused, please authorize this script in skype to listen to incoming messages"
	elif status == sky.apiAttachNotAvailable:
		print "no api hook available"
			
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

while True:
	time.sleep(1)
