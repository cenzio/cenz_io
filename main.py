from bot.bot import Bot

if __name__ == "__main__":
	cenz = TwitterBot('data/bot_config.txt')
	cenz.create_status("random")
	cenz.shutdown()