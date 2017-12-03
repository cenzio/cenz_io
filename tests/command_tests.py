import unittest
from logger import Logger
from bot.bot import Bot

class CommandTests(unittest.TestCase):
	"""
	unit testing default bot commands
	"""
	def setUp(self):
		self.bot= Bot('data/bot_config.txt')
		
	def test_hello_world(self):
		"""
		Test the hello world command
		"""
		output = self.bot.hello_command()
		self.assertEqual(output, "Hello, world!")
		Logger

	def test_about_command(self):
		"""
		Test the about command
		"""
		output = self.bot.about_command()

		api = self.bot.get_me()

		info_list = []
		info_list.append('Name: ' + str(bot_info.screen_name) +'\n')
		info_list.append('Desc: ' + str(bot_info.description) + '\n')
		info_list.append('Friends: ' + str(bot_info.friends_count) + '\n')
		info_list.append('Created: ' + str(bot_info.created_at) + '\n')
		info_list.append('Verified: ' + str(bot_info.verified) + '\n')
		info_list.append('URL: ' + str(bot_info.url) +'\n')
		info_list.append('Version: cenz_io-v1.0')
		
		self.assertEqual(output, "".join(info_list))
		print("about command works")


if __name__ == '__main__':
	unittest.main()
