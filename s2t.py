import Skype4Py as sky
import time
import re
				

class SkypeListener(object):

	def __init__(self, chats_to_follow, key_expressions = { }):
		self.chats_to_follow = chats_to_follow
		self.key_expressions = key_expressions

		self.hook = sky.Skype()
		self.hook.OnAttachmentStatus = self.attachment_status_change;
		self.hook.OnMessageStatus = self.message_status_change;	

	def attach(self):
		print "connecting to skype....."
		self.hook.Attach()

	def attachment_status_change(self, status):					# event handler for local attachment to skype
		print "API attachment status changed to: " + self.hook.Convert.AttachmentStatusToText(status)
		if status == sky.apiAttachAvailable:
			self.hook.Attach();
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


	def message_status_change(self, message, status):				# event handler for messages
		if str(message.Chat.Topic) in self.chats_to_follow:
			if status == 'RECEIVED' or status == 'SENT':
				self.parse_message(message)
		

	def parse_message(self, message):
		msg = message.Body							# get the text of the message
		for k, v in self.key_expressions.iteritems():
			m = re.search(str(k), msg)						# look for each of the given regular expressions in the message, if no match is found, m will be None
			print msg, k, m
			if m:
				v(msg[m.start():len(msg)].strip())			# get the message body without the prefix and surrounding whitespaces and call the given method	
			

def post_on_tumblr(message):
	pattern = "http://www.\S{1,}\.[a-zA-Z]{2,3}"
	print "baem tumblr"


if __name__ == "__main__":


	chats_to_follow = ("The High Council of Disposia")
	key_expressions = {"\b<tumb>\b" : post_on_tumblr }
	

	print "skype2tumblr started, initializing..."
	listener = SkypeListener(chats_to_follow, key_expressions)	
	listener.attach()									# connect to api hook

	while True:										# wait for new message events
		time.sleep(1)
