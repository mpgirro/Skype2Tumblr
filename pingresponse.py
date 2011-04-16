import re

class PingResponse(object):

	def __init__(self):
		self.match = ("^ping(!)*$",)

	def init(self, chats):
		return

	def shutdown(self, chats):
		return

	def notify(self, message):
		body = message.Body
		for exp in self.match:
			if re.search(exp, body):
				message.Chat.SendMessage("[Auto Ping Response]: pong" + "!"*body.count("!"))


def getinstance():
	return PingResponse()
