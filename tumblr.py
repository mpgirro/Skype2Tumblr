import re


class Tumblr(object):

	def __init__(self, account = "", password = "", accfilename = None):
		'''creates a new Tumblr object with the given accountname and password, to not have to write the login data in here 
		the additional option to read it from an external file is given'''
		if accfilename:
			accfile = open(accfilename, "r")						# open file with account information
			self.account = accfile.readline()[:-1]						# first line = email
			self.password = accfile.readline()[:-1]						# second line = password
			accfile.close()									# close file
		else:
			self.account = account
			self.password = password
		self.urlpattern = "(http://)?(www\.)?\S+\.[a-zA-Z]{2,3}(/(\S+/?)*)?"			# pattern for recognising a url
		self.expression_matches = ("^<tumb> ",)							# patterns that should be matched when parsing messages


	def messageevent(self, message):								# event listner method for messages
		for exp in self.expression_matches:							# check if any expression matches
			msg = message.Body									
			m = re.search(exp, msg)		
			if m:										# if it matches, post the content of the message on tumblr
				self.post(message, msg[m.end():len(msg)].strip())	
		

	def post(self, message, content):	
		'''posts the given message to a tumblog specified by account, before doing so it will parse the message for a url.
		if a url is found, it will send it to tumblr to analyse it and collect relevant data before sending it via the html api'''
		match = re.search(self.urlpattern, content)						# check if there is a url in the message

		url = "http://www.tumblr.com/"
		caption = " ( by " + message.FromDisplayName + " via Skype) "

		if match:										# if a url is in the message
			if match.start() > 0:								# if there is a comment before the url
				caption = content[:match.start()].strip() + caption			# get the comment
			posturl = content[match.start():match.end()]					# get the url
			#tumblrtype = "regular"
			#title = caption
			#body = posturl
		elif len(content) > 0:									# if there is no url in the message
			tumblrtype = "quote"								# take the string and post it as quote
			quote = content
		else:											# if the content of the message is empty
			print "could not find anything to post in the given message: " + content

		#if apiurl:
		#	pass
			#open api url, else, do nothing and return

	def skypepost(self, chat, message):								# dummy object for posting on skype, should be overwritten
		pass


def getinstance():
	return Tumblr(accfilename="tumblr.txt")
