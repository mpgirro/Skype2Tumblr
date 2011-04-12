import re
import urllib2
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup


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
		self.urlopener = None
		self.urlpattern = "(http://)?(www\.)?\S+\.[a-zA-Z]{2,3}(/(\S+/?)*)?"			# pattern for recognising a url
		self.expression_matches = ("^<tumb> ",)							# patterns that should be matched when parsing messages
		self.string_replacements = { "&#039;" : "\'", "&quot;" : "\"", "&lt;" : "<", "&gt;" : ">" }


	def messageevent(self, message):								# event listner method for messages
		for exp in self.expression_matches:							# check if any expression matches
			msg = message.Body									
			m = re.search(exp, msg)		
			if m:										# if it matches, post the content of the message on tumblr
				self.post(message, msg[m.end():len(msg)].strip())	

	def login(self):
		postdata = {"user[email]" : self.account, "user[password]" : self.password}
		request = urllib2.Request("http://www.tumblr.com", urllib.urlencode(postdata))
		cookiejar = cookielib.CookieJar()
		self.urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
		self.urlopener.open(request)
		self.urlopener.login_success = True							# custom attribute
		
		#for cookie in cookiejar:
		#	print cookie
		#	if cookie.name == "logged_in" and cookie.value == "1":
		#		print "tumblr.login(): successfully logged in"
		#		self.urlopener.login_success = True
		#		return True
		#print "tumblr.login(): error logging in"
		return True
		

	def post(self, message, content):	
		'''posts the given message to a tumblog specified by account, before doing so it will parse the message for a url.
		if a url is found, it will send it to tumblr to analyse it and collect relevant data before sending it via the html api'''

		caption = "\n\n(by " + message.FromDisplayName + " via Skype)"

		if not self.urlopener:
			self.login()
		#if not self.urlopener.login_success or self.login():
		#	print "tumblr.post(): connection to tumblr could not be established...aborting"
		#	print self.urlopener.login_success
		#	return

		match = re.search(self.urlpattern, content)						# check if there is a url in the message

		if match:										# if a url is in the message
			if match.start() > 0:								# if there is a comment before the url
				caption = content[:match.start()].strip() + caption			# get the comment
			posturl = content[match.start():match.end()]					# get the url
			post_attributes = self.gather_post_data(posturl, caption)
			post_request = urllib2.Request("http://www.tumblr.com/share", urllib.urlencode(post_attributes))
			self.urlopener.open(post_request)
			print "successfully posted on tumblr"
			message.Chat.SendMessage("successfully posted on tumblr")
		elif len(content) > 0:									# if there is no url in the message
			print "could not post quote, feature not yet implemented"
			message.Chat.SendMessage("could not post quote, feature not yet implemented")
			self.post_via_api(content)
		else:											# if the content of the message is empty
			print "tumblr.post(): could not find anything to post in the given message: " + content


	def gather_post_data(self, url, custom_caption):
		req_string = "http://www.tumblr.com/share?v=3&u=" + urllib.quote(url)
		request = urllib2.Request(req_string)
		soup = BeautifulSoup(self.urlopener.open(request))
		
		input_elements = { }
		forms = soup.findAll("form")
		for form in forms:
			if not form.get("style"):
				inputs = form.findAll("input")
				for input_el in inputs:
					input_elements[input_el.get("name")] = input_el.get("value")

		caption_element = soup.find("textarea", { "id" : "video_post_two" })
		caption = caption_element.contents[0]

		for k, v in self.string_replacements.iteritems():
			caption = caption.replace(k, v)

		input_elements[caption_element.get("name")] = caption + "\n\n" + custom_caption

		return input_elements


	def post_via_api(self, message):
		pass



def getinstance():
	return Tumblr(accfilename="tumblr.txt")
