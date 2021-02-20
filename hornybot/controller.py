from hornybot.web_driver import *

class BOT:
	def __init__(self, username=False, email=False, password=False, log=False, load_session=False, login=False):
		self.log = log
		self.driver = DRIVER(username=username, email=email, password=password, options=False)

		if login:
			self.driver.login()
		else:
			if load_session:
				self.driver.load_session()

	def login(self, username=False, password=False, save_cookies=True):
		self.driver.login(username=username, password=password)
		if save_cookies:
			self.driver.save_session()

	def get_stories(self, username):
		return self.driver.get_stories(username)

	def get_highlights(self, username):
		return self.driver.get_highlights(username)

	def get_posts(self, username):
		return self.driver.get_posts(username)

	def download(self, username):
		self.driver.download(username)
