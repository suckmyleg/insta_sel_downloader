from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import time
import json
import random
import wget
import os
from webdriver_manager.chrome import ChromeDriverManager

class DRIVER:
	def open_web(self, options=False):
		options_obj = webdriver.ChromeOptions()
		if options or self.options:
			options_obj.binary_location = "/usr/bin/chromium-browser"
			options_obj.add_argument("--no-sandbox")
			options_obj.add_argument("--disable-dev-shm-usage")
			options_obj.add_argument("--disable-setuid-sandbox")
			options_obj.add_argument("--remote-debugging-port=9222")
			options_obj.add_argument("--disable-dev-shm-using")
			options_obj.add_argument("--disable-extensions") 
			options_obj.add_argument("--disable-gpu") 
			options_obj.add_argument("start-maximized") 
			options_obj.add_argument("disable-infobars") 
			options_obj.add_argument("--headless")

		self.web = webdriver.Chrome(ChromeDriverManager().install(), options=options_obj)

	def close_web(self):
		if self.web:
			self.web.quit()
			self.web = False

	def load_cookies(self):
		domains = []
		for cookie in self.cookies:
			try:

				domain = cookie["domain"]

				if not "www" in domain:
					domain = "www" + domain

				visited = False

				for d in domains:
					if d == domain:
						visited = True

				if not visited:
					self.web.get("https://" + domain)
					domains.append(domain)

				self.web.add_cookie(cookie)

			except Exception as e:
				print(e, domain)
		self.logged = True

	def load(self):
		if not self.web:
			self.open_web()
		if self.cookies:
			self.load_cookies()
		else:
			self.login()

	def get_cookies(self):
		if self.web:
			return self.web.get_cookies()
		else:
			return []

	def load_cookies_from_session(self):
		try:
			self.cookies = json.loads(open("session.json", "r").read())
		except:
			self.cookies = []

	def load_session(self):
		if not self.web:
			self.open_web()
		self.load_cookies_from_session()
		self.load_cookies()
		self.remove_notify_button()

	def save_session(self):
		open("session.json", "w").write(json.dumps(self.get_cookies()))

	def logout(self):
		while True:
			try:
				self.web.get("https://www.instagram.com/")

				self.ti(1)

				print("Logging out")

				self.web.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span').click()

				self.ti(2)

				keys = ['//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div',
				'//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]']

				logoutbutton = self.find_element_by_xpath(keys)

				if not logoutbutton:
					logoutbutton = self.web.find_element_by_class_name('-qQT3')


				logoutbutton.click()

				self.logged = False

			except Exception as e:
				print(e)

	def login_info(self):
		datas = [
		["username", self.username],
		["password", self.password],
		["web", self.web],
		["options", self.options]
		]
		for d in datas:
			print("{} = {}".format(d[0], d[1]))

	def remove_notify_button(self):
		self.web.get("https://www.instagram.com/")
		for i in range(10):
			keys = [
			'/html/body/div[4]/div/div/div/div[3]/button[2]',
			'//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]']

			annoyingNotifyButton = self.find_element_by_xpath(keys)

			if not annoyingNotifyButton:
				try:
					annoyingNotifyButton = self.web.find_element_by_class_name('-qQT3')
				except:
					pass

			if annoyingNotifyButton:
				annoyingNotifyButton.click()
				break

			self.ti(1)

	def get_data_from_instagram(self, instagram):
		try:
			data = self.data[instagram]
		except:
			data = {"urls":[]}
			self.data[instagram] = data

		return data


	def login(self, username=False, password=False):
		if username:
			self.username = username
		if password:
			self.password = password

		if not (self.username or self.email) or not self.password:
			print("Username, email or password variable missing.\nPls use 'username'/'email' and 'password' to login or 'cookies' to load account.")
			return False
		while True:
			try:
				self.web.get("https://www.instagram.com/")

				self.ti(1)

				print("Logging in")

				try:
					annoyingCookiesButton = self.web.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]')

					annoyingCookiesButton.click()
				except:
					pass

				self.ti(1)

				try:
					usernameInput = self.web.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')

				except:
					usernameInput = self.web.find_element_by_name('username')

				try:
					passwordInput = self.web.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')

				except:
					passwordInput = self.web.find_element_by_name('password')

				submitButton = self.web.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')

				usernameInput.send_keys(self.username)

				passwordInput.send_keys(self.password)

				submitButton.click()

				self.ti(3)

				self.remove_notify_button()

				self.logged = True

				print("Logged")

				return True

			except Exception as e:
				print(e)
				self.logout()
				self.login()
				return True


	def go_to_profile(self, username):
		self.web.get("https://www.instagram.com/" + username)
		self.ti(2)

	def say(self, message):
		print("{}: {}".format("web_driver", message))

	def new_story(self, url, type, media_type):
		return {"url":url, "type":type, "media_type":media_type, "bot":self.username, "downloaded":False}

	def add_story(self, username, url, type, media_type):
		urls = self.get_data_from_instagram(username)["urls"]

		urls.append(self.new_story(url, type, media_type))

		self.data[username]["urls"] = urls


	def find_element_by_xpath(self, keys):
		output = False
		for k in keys:
			try:
				#self.say("Trying to find element with key: {}".format(k))
				output = self.web.find_element_by_xpath(k)
			except:
				pass
				#self.say("Failed\n")
			else:
				if output:
					break
		return output

	def get_follow_button(self):
		keys = ['//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button',
		'//*[@id="react-root"]/section/main/div/header/section/div[2]',
		'//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button',
		'//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button',
		'//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button']

		return self.find_element_by_xpath(keys)

	def get_img_from_story(self):
		keys = ['//*[@id="react-root"]/section/div/div/section/div[2]/div[1]/div/div/img',
		'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/img',
		'//*[@id="react-root"]/section/div[1]/div/div[5]/section/div/div[1]/div/div/img']

		return self.find_element_by_xpath(keys)

	def get_video_from_story(self):
		keys = ['//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video/source[1]',
		'//*[@id="react-root"]/section/div[1]/div/section/div/div[1]/div/div/video/source[3]',
		'//*[@id="react-root"]/section/div[1]/div/div[5]/section/div/div[1]/div/div/video/source'
		]

		return self.find_element_by_xpath(keys)

	def get_post(self):
		try:
			url = self.web.find_element_by_class_name('FFVAD')
		except:
			try:
				url = self.web.find_element_by_class_name('tWeCl')
				type = "vid"
			except:
				pass
		else:
			type = "img"

		return [url.get_attribute("src"), type]


	def get_content(self):
		content = self.get_video_from_story()

		type = "vid"

		if not content:
			content = self.get_img_from_story()

			type = "img"

			urls = content.get_attribute("srcset").split("https")

			url = "https" + urls[1][:len(urls[1])-1].replace(" ", "").replace("1080w", "")

		else:
			url = content.get_attribute("src")
		return [url, type]

	def get_next_button(self):
		keys = ['//*[@id="react-root"]/section/div[1]/div/div[5]/section/div/button[2]/div',
		'//*[@id="react-root"]/section/div[1]/div/div[5]/section/div/button/div',
		'/html/body/div[1]/section/div/div/section/div[2]/button[2]/div',
		'//*[@id="react-root"]/section/div/div/section/div[2]/button[2]/div',
		'//*[@id="react-root"]/section/div[1]/div/section/div/button[2]/div',
		'/html/body/div[1]/section/div/div/section/div[2]/button[2]',
		'/section/div[2]/button[2]/div'
		]

		nextButton = self.find_element_by_xpath(keys)

		if not nextButton:
			try:
				nextButton = self.web.find_element_by_css_selector('#react-root > section > div > div > section > div.GHEPc > button.ow3u_ > div')	
			except:
				try:
					nextButton = self.web.find_element_by_class_name('coreSpriteRightChevron')
				except:
					nextButton = False

		return nextButton



	def get_urls_from_web(self, username, log=True, type="Uknown", mode="story"):
		try:
			nextButton = self.try_function(self.get_next_button, 1)
			self.ti(0.5)
			if log:
				self.say("Getting urls from {}s".format(mode))
			nn = 0
			cloned_url = 0
			last_url = ""
			while True:
				try:
					if mode == "story":
						r = self.try_function(self.get_content, 1)
					else:
						r = self.try_function(self.get_post, 1)

					url = r[0]

					if r:
						if url == last_url:
							cloned_url += 1
						else:
							cloned_url = 0
							last_url = url

						if cloned_url == 3:
							break

						media_type = r[1]

						self.add_story(username, url, type, media_type)
					
					nn += 1

					nextButton = self.try_function(self.get_next_button, 1)

					self.try_function(nextButton.click, 1, returnn=False)

					nextButton = self.try_function(self.get_next_button, 1)
				except Exception as e:
					break

			if nn > 0:
				if log:
					self.say("" + str(nn) + " stories")
			else:
				if log:
					self.say("No stories")
		except Exception as e:
			if log:
				self.say(e)

		return self.get_data_from_instagram(username)



	def try_function(self, fun, timee, arg=False, returnn=True):
		times = timee * 10
		delay = timee/times
		result = False
		i = 0
		while not result:
			try:
				if arg:
					if returnn:
						result = fun(arg)
					else:
						fun(arg)
				else:
					if returnn:
						result = fun()
					else:
						fun()
			except Exception as e:
				#print(e)
				result = False
			else:
				if not returnn:
					break
			i += 1
			if i == times or result:
				return result
			else:
				time.sleep(delay)

	def ti(self, s):
		n = (random.randint(0, 100) / 100) + s
		#print("Sleeping:" + str(n))
		time.sleep(n)

	def click_story(self):
		try:
			historyButton = self.web.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/div/div')

			historyButton.click()
			return True
		except Exception as e:
			print(e)
			return False

	def get_highlights(self, username):
		if self.logged:
			self.go_to_profile(username)

			try:
				elements = self.web.find_elements_by_class_name('Ckrof')
			except:
				elements = []

			data = {}

			for e in elements:
				try:
					e.click()
				except:
					pass
				else:
					data = self.get_urls_from_web(username, type="highlight")

			self.ti(1)

			return data
		else:
			print("You need to log in to an account to use get_highlights")

	def get_posts(self, username):
		if self.logged:
			self.go_to_profile(username)

			try:
				elements = self.web.find_elements_by_class_name('_9AhH0')
			except:
				elements = []

			data = {}

			for e in elements:
				try:
					e.click()
				except:
					pass
				else:
					data = self.get_urls_from_web(username, type="post", mode="post")

					webdriver.ActionChains(self.web).send_keys(Keys.ESCAPE).perform()

			self.ti(1)

			return data
		else:
			print("You need to log in to an account to use get_highlights")

	def get_stories(self, username):
		if self.logged:
			self.go_to_profile(username)

			data = {}

			if self.click_story():
				data = self.get_urls_from_web(username, type="story")

			self.ti(1)

			return data
		else:
			print("You need to log in to an account to use get_stories")

	def download(self, username):
		try:
			ll = len(self.get_data_from_instagram(username)["urls"])
		except:
			return False

		o = 0
		for i in self.get_data_from_instagram(username)["urls"]:
			o += 1
			try:
				try:
					os.mkdir(username)
				except:
					pass

				try:
					url = i["url"]
				except:
					url = i

				fileinfo = urlparse(url)

				if not os.path.exists(username + "/"):
					try:
						os.mkdir(username)
					except:
						pass

				path = username + "/" + str(os.path.basename(fileinfo.path))

				if not os.path.exists(path):
					try:
						wget.download(url, path)
					except Exception as e:
						print(e)

				print(" " + username, "{}/{}".format(o, ll))

			except Exception as e:
				print(e)
			time.sleep(0.01)

	def __init__(self, username=False, email=False, password=False, cookies=[], auto_load=False, options=False, auto_open_web=True):
		self.username = username
		self.email = email
		self.password = password
		self.cookies = cookies
		self.logged = False
		self.web = False
		self.auto_load = auto_load
		self.options = options
		self.data = {}
		self.auto_open_web = auto_open_web

		if self.auto_open_web:
			self.open_web(self.options)
		if self.auto_load:
			self.load()
