import Skype4Py as sky
import time
import re
				

def attachment_status_change(status):						# event handler for local attachment to skype

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
			
def message_status_change(message, status):					# event handler for messages
	global chats_to_follow

	if str(message.Chat.Topic) in chats_to_follow:
		if status == 'RECEIVED' or status == 'SENT':
			parse_message(message)



def parse_message(message):
	global key_expressions
	
	msg = message.Body							# get the text of the message
	for k, v in key_expressions.iteritems():
		m = re.search(k, msg)						# look for each of the given regular expressions in the message, if no match is found, m will be None
		if m:
			v(msg[m.start():len(msg)].strip())			# get the message body without the prefix and surrounding whitespaces and call the given method	
			

def post_on_tumblr(message):
	pattern = "http://www.\S{1,}\.[a-zA-Z]{2,3}

###############
chats_to_follow = ("The High Council of Disposia")
key_expressions = {"\b<tumb>\b" : post_on_tumblr}
###############
	

print "skype2tumblr started, initializing..."
client = sky.Skype()
client.OnAttachmentStatus = attachment_status_change;				# set event handler for api hook
client.OnMessageStatus = message_status_change;					# set event handler for message status

print "connecting to skype....."
client.Attach()									# connect to api hook

while True:									# wait for new message events
	time.sleep(1)
