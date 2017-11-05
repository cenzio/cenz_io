from bot.bot import Bot

if __name__ == "__main__":
	cenz = Bot('data/bot_config.txt')
	cenz.create_status("this is a test")