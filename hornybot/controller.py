from hornybot.web_driver import *
from cryptography.fernet import Fernet

class BOT:
	def __init__(self, username=False, email=False, password=False, log=False, load_session=False, login=False, encrypt_key=False):
		self.log = log
		self.driver = DRIVER(username=username, email=email, password=password, options=False)

		self.fernet = False

		if encrypt_key:
			self.fernet = Fernet(encrypt_key)

		if login:
			self.driver.login()
		else:
			if load_session:
				self.driver.load_session()

	def login(self, username=False, password=False, save_cookies=True):
		self.driver.login(username=username, password=password)
		if save_cookies:
			self.driver.save_session()

	def encrypt(self, path):
		if ".mp4" in path or ".png" in path or ".jpg" in path:
			self.driver.encrypt(path, self.fernet)

	def decrypt(self, path):
		if ".mp4" in path or ".png" in path or ".jpg" in path:
			self.driver.decrypt(path, self.fernet)

	def encrypt_i(self, i):
		content = os.scandir(i+"/")

		for c in content:
			self.encrypt(i+"/"+c.name)

	def decrypt_i(self, i):
		content = os.scandir(i+"/")

		for c in content:
			self.decrypt(i+"/"+c.name)

	def get_stories(self, username):
		return self.driver.get_stories(username)

	def get_highlights(self, username):
		return self.driver.get_highlights(username)

	def get_posts(self, username):
		return self.driver.get_posts(username)

	def download(self, username):
		self.driver.download(username, encrypt=self.fernet)
