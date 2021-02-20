# How to use
```python
import hornybot

bot = hornybot.BOT(username, password)

bot.login(username="your_instagram_username_account", password="your_instagram_username_password")

bot.get_stories("instagram_username")
bot.get_highlights("instagram_username")
bot.get_posts("instagram_username")

bot.download("instagram_username")
```

# Login

Login to save cookies
```python
import hornybot

bot = hornybot.BOT(username, password)

bot.login(username="your_instagram_username_account", password="your_instagram_username_password")
```

Load cookies
```python
import hornybot

bot = hornybot.BOT(username, password)

bot.load_session()
```

# Get data
You can get a json object with info of the url by adding the return value of the function to a variable. 
```python
import hornybot

bot = hornybot.BOT(username, password)

data = bot.get_stories("instagram_username")
data = bot.get_highlights("instagram_username")
data = bot.get_posts("instagram_username")
```

Each function returns all the urls from the instagram_user. 

BOT object saves urls to a json variable, each time you get posts or stories from someone, you're saving the urls to a json inside a variable with the name of the instagram you're getting the urls from, so if you do a get_stories and then a get_highlights, the urls from get_stories will came also from get_higligths.

Example:

```python
import hornybot

bot = hornybot.BOT(username, password)

data = bot.get_stories("instagram_username")

data =	{"urls":
			[
				{"url":"url1", "type":"story"}
			]
		}




data = bot.get_highlights("instagram_username")

data =	{"urls":
			[
				{"url":"url1", "type":"story"},
				{"url":"url2", "type":"highlight"}
			]
		}


```

# Arguments accepted by BOT object
|Argument|Default|Variable|Do|
|--------|-------|--------|--|
|username|False|Bool|If true: Login with that username|
|email|False|Bool|Does nothing|
|password|False|Bool|If true: Login with that password|
|load_session|False|Bool|If true: auto load cookies|
|login|False|Bool|If true: auto login|
|log|False|Bool|Display log messages|
