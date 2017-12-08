import unittest
from bot.bot import TwitterBot

class CommandTests(unittest.TestCase):
	"""
	unit testing default bot commands
	"""
	def setUp(self):
		self.bot= TwitterBot('data/bot_config.txt')
		
	def test_hello_world(self):
		"""
		Test the hello world command
		"""
		output = self.bot.hello_command()
		self.assertEqual(output, "Hello, world!")
		print("hello command works")

	def test_about_command(self):
		"""
		Test the about command
		"""
		output = self.bot.about_command()
		bot_info = self.bot.get_me()

		info_list = []
		info_list.append('Name: ' + str(bot_info.screen_name) +'\n')
		info_list.append('Desc: ' + str(bot_info.description) + '\n')
		info_list.append('Friends: ' + str(bot_info.friends_count) + '\n')
		info_list.append('Created: ' + str(bot_info.created_at) + '\n')
		info_list.append('Verified: ' + str(bot_info.verified) + '\n')
		info_list.append('URL: ' + str(bot_info.url) +'\n')
		info_list.append('Version: cenz_io-v1.0')
		
		self.assertEqual(output, "".join(info_list))
		print("About command works")

	def test_help_command(self):
		"""
		Test out all the commands inside the twitter bot
		"""
		all_command_intro = "Here are all the commands that I have:\n"
		command_help = ["!hello - Returns a simple hello world!\n",
					 	"!about - Returns information about the bot.\n",
					 	"!8ball - Returns a accurate predictions from the magical 8ball\n"]
		command_help_string = all_command_intro + "".join(command_help)
		
		all_help = self.bot.help_command()
		self.assertEqual(all_help, command_help_string)
		print("Calling the help command without a parameter works")

		index = 0
		for command in ['!hello', '!about', '!8ball']:
			self.assertEqual(self.bot.help_command(command), command_help[index])
			index += 1
		print("Calling the help command with a parameter works")
		
if __name__ == '__main__':
	unittest.main()
