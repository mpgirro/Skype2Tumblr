import Skype4Py as sky
import time
import re
import tumblr
import pingresponse
import existencenotifier
				

class SkypeListener(object):

	def __init__(self, chats_to_follow, message_listeners = ()):
		'''creates a new SykpeListner object which will follow the chats specified in chats_to_follow (tuple) and look for 
		the given regular expressions specified in key_expresssions (dict), if an expression was matched, the corresponding listener 
		method given in the dictionary will be called'''

		self.chats_to_follow = chats_to_follow						
		self.message_listeners = message_listeners

		self.hook = sky.Skype()
		self.hook.OnAttachmentStatus = self.attachment_status_change;					# set the listener method for attachment status changes
		#self.hook.OnMessageStatus = self.message_status_change;						# set the listener method for message status changes

	def attach(self):		
		'''attaches the Skype object to the local Skype api hook'''
		print "connecting to skype....."
		self.hook.Attach()
		self.chats = []
		for chat in self.hook.Chats:
			if str(chat.Topic) in self.chats_to_follow:
				self.chats.append(chat)
				chat.last_id = chat.Messages[0].Id

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


	def process_messages(self):	
		for chat in self.chats:	
			msgs = chat.Messages
			for message in msgs:
				if message.Id == chat.last_id:
					break
				print message.FromDisplayName + ":", message.Body				
				print "-------------------------------------------------------"
				for listener in self.message_listeners:						# invoke the messageevent method for all listeners
					listener.notify(message)
			chat.last_id = msgs[0].Id




if __name__ == "__main__":

	tumb = tumblr.getinstance()
	pingre = pingresponse.getinstance()
	enotify = existencenotifier.getinstance()

	chats_to_follow = ("The High Council of Disposia",)
	message_listeners = (tumb, pingre, enotify)

	print "skype2tumblr started, initializing..."
	listener = SkypeListener(chats_to_follow, message_listeners)	
	listener.attach()									# connect to api hook

	while True:										# wait for new message events
		listener.process_messages()
		time.sleep(10)
