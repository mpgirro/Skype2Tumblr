import re

class ExistenceNotifier(object):

	def __init__(self):
		self.match = ("^s2t[!\?]*$", "^bot active\?*$", "^bot alive\?*$" )

	def notify(self, message):
		body = message.Body
		for exp in self.match:
			if re.search(exp, body):
				message.Chat.SendMessage("[Skype2Tumblr]: at your service oh great one!")


def getinstance():
	return ExistenceNotifier()
