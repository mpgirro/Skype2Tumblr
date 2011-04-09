import Skype4Py as sky
import time
import re
				

class SkypeListener(object):

	def __init__(self, chats_to_follow, message_listeners = ()):
		'''creates a new SykpeListner object which will follow the chats specified in chats_to_follow (tuple) and look for 
		the given regular expressions specified in key_expresssions (dict), if an expression was matched, the corresponding listener 
		method given in the dictionary will be called'''

		self.chats_to_follow = chats_to_follow
		self.message_listeners = message_listeners

		self.hook = sky.Skype()
		self.hook.OnAttachmentStatus = self.attachment_status_change;
		self.hook.OnMessageStatus = self.message_status_change;	

	def attach(self):
		'''attaches the Skype object to the local Skype api hook'''
		print "connecting to skype....."
		self.hook.Attach()

	def attachment_status_change(self, status):					
		'''this is the event handler method for the local attachment to skype, it will automatically connect or reconnect to Skype if Skype
		was shutdown and restarted or if the script was started before Skype'''

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


	def message_status_change(self, message, status):				
		'''this is the event handler method for messages, if a new message is received or sent, it will call all listening methods'''
		if str(message.Chat.Topic) in self.chats_to_follow:
			if status == 'RECEIVED' or status == 'SENT':
				for listener in self.message_listeners:
					listener(message)
		


class Tumblr(object):

	def __init__(self, account = "", password = "", accfilename = None):
		'''creates a new Tumblr object with the given accountname and password, to not have to write the login data in here 
		the additional option to read it from an external file is given'''
		if accfilename:
			accfile = open(accfilename, "r")
			self.account = accfile.readline().strip("\n")
			self.password = accfile.readline().strip("\n")
			accfile.close()
		else:
			self.account = account
			self.password = password
		self.urlpattern = "(http://)?(www\.)?\S+\.[a-zA-Z]{2,3}(/(\S+/?)*)?"
		self.expression_matches = ("^<tumb> ",)

	def match(self, message):
		for exp in self.expression_matches:
			msg = message.Body		
			m = re.search(exp, msg)		
			if m:
				self.post(msg[m.end():len(msg)].strip(), str(message.Sender.DisplayName))	
		

	def post(self, message, sender):	
		'''posts the given message to a tumblog specified by account, before doing so it will parse the message for a url.
		if a url is found, it will send it to tumblr to analyse it and collect relevant data before sending it via the html api'''
		match = re.search(self.urlpattern, message)

		url = "http://www.tumblr.com/"
		caption = " ( by " + sender + " via Skype) "

		print match, message
		if match:
			if match.start() > 0:
				caption = message[:match.start()].strip() + caption
			posturl = message[match.start():match.end()]
			#tumblrtype = "regular"
			#title = caption
			#body = posturl
		elif len(message) > 0:
			tumblrtype = "quote"
			quote = message
		else:
			print "could not find anything to post in the given message: " + message

		#if apiurl:
		#	pass
			#open api url, else, do nothing and return

	


if __name__ == "__main__":

	tumblr = Tumblr(accfilename="tumblr.txt")

	chats_to_follow = ("The High Council of Disposia")
	message_listeners = (tumblr.match,)

	print "skype2tumblr started, initializing..."
	listener = SkypeListener(chats_to_follow, message_listeners)	
	listener.attach()									# connect to api hook

	while True:										# wait for new message events
		time.sleep(1)
