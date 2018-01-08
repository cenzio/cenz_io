from bot.bot import TwitterBot

if __name__ == "__main__":
	cenz = TwitterBot('data/bot_config.txt')
	cenz.create_status("yoo")
	cenz.shutdown()