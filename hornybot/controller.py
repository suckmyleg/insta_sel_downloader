from hornybot.web_driver import *
from cryptography.fernet import Fernet
from json import loads, dumps

class BOT:
	def __init__(self, username=False, email=False, password=False, log=False, load_session=False, login=False, encrypt_key=False):
		self.log = log
		self.driver = DRIVER(username=username, email=email, password=password, options=False)

		self.data = {"instagrams":{}}

		self.fernet = False

		if encrypt_key:
			self.fernet = Fernet(encrypt_key)

		if login:
			self.driver.login()
		else:
			if load_session:
				self.driver.load_session()

	def add_insta(self, instagram):
		self.data["instagrams"][instagram]{"instagram":instagram, "data":[]}

	def load_data(self):
		try:
			self.data = loads(self.fernet.decrypt(open(self.file_data_location, "r").read()))
		except:
			self.save_data()

	def save_data(self):
		open(self.file_data_location, "r").write(self.fernet.encrypt(dumps(self.data)))

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
		for f in self.driver.download(username, encrypt=False):
			with open(f, "r") as file:

				data = file.read()

				file_data = {""}

				if not data in self.data["instagrams"][username]["data"]

