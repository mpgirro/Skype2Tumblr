import re

class ExistenceNotifier(object):

	def __init__(self):
		self.match = ("^s2t[!\?]*$", "^bot active\?*$", "^bot alive\?*$" )
	
		self.MSG_STARTUP = 	"[Skype2Tumblr]: I am ALIVE!"
		self.MSG_SHUTDOWN = 	"[Skype2Tumblr]: Systems, shutting, doowwwwwwwwwn"
		self.MSG_EXIST = 	"[Skype2Tumblr]: At your service oh great one!"

	def init(self, chats):
		for chat in chats:
			chat.SendMessage(self.MSG_STARTUP)

	def shutdown(self, chats):
		for chat in chats:
			chat.SendMessage(self.MSG_SHUTDOWN)

	def notify(self, message):
		body = message.Body
		for exp in self.match:
			if re.search(exp, body):
				message.Chat.SendMessage(self.MSG_EXIST)


def getinstance():
	return ExistenceNotifier()
