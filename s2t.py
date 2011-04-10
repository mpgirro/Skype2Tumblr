import Skype4Py as sky
import time
import re
import tumblr
				

class SkypeListener(object):

	def __init__(self, chats_to_follow, message_listeners = ()):
		'''creates a new SykpeListner object which will follow the chats specified in chats_to_follow (tuple) and look for 
		the given regular expressions specified in key_expresssions (dict), if an expression was matched, the corresponding listener 
		method given in the dictionary will be called'''

		self.chats_to_follow = chats_to_follow						
		self.message_listeners = message_listeners

		for listener in self.message_listeners:								# set the post methods for all listeners so they can post something on skype
			listener.skypepost = self.skypepost

		self.hook = sky.Skype()
		self.hook.OnAttachmentStatus = self.attachment_status_change;					# set the listener method for attachment status changes
		self.hook.OnMessageStatus = self.message_status_change;						# set the listener method for message status changes

	def attach(self):		
		'''attaches the Skype object to the local Skype api hook'''
		print "connecting to skype....."
		self.hook.Attach()

	def attachment_status_change(self, status):					
		'''this is the event handler method for the local attachment to skype, it will automatically connect or reconnect to Skype if Skype
		was shutdown and restarted or if the script was started before Skype'''

		print "API attachment status changed to: " + self.hook.Convert.AttachmentStatusToText(status)	
		if status == sky.apiAttachAvailable:								
			while True:			
				try:
					print "connecting to Skype..."
					self.hook.Attach();
					break
				except ISkypeAPIError:
					print "connection to Skype timed out, trying again..."

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
		if str(message.Chat.Topic) in self.chats_to_follow:						# if the message was posted in a followed chat
			if status == 'RECEIVED' or status == 'SENT':						# if the message was sent or received
				print message.FromDisplayName + ":", message.Body				
				print "-------------------------------------------------------"
				for listener in self.message_listeners:						# invoke the messageevent method for all listeners
					listener.messageevent(message)

	def skypepost(self, chat, message):
		'''method for posting on skype, all listening classes will receive this method upon object creation and
		can then post on skype via this method'''
		if chat:
			chat.SendMessage(message)
				
		



if __name__ == "__main__":

	tumb = tumblr.getinstance()

	chats_to_follow = ("The High Council of Disposia",)
	message_listeners = (tumb,)

	print "skype2tumblr started, initializing..."
	listener = SkypeListener(chats_to_follow, message_listeners)	
	listener.attach()									# connect to api hook

	while True:										# wait for new message events
		time.sleep(1)
