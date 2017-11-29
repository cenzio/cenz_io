"""
Module for running the cenz_io multifunctional twitter bot
"""
import tweepy
from tweepy import TweepError, RateLimitError
import time

from random import randint
from bot.message import MessageNode, MessageQueue

class Bot(object):
	"""
	Twitter bot that will be used to receive and act on commands
	You can create multiple bots if you'd like but there is no support
	for running multiple bots at the same time within the same program
	"""

	def __init__(self, config_file):
		"""
		Params:
			(str) config: the tweepy api for the specific user you want to link the bot to
		
		Variables:
			(bool) bot_running: Whether the bot is active and running or not
			(CommandManager) command_man: the commands available to the user
			(int) last_checked_message: id of the last dm received
		"""

		#Authenticate with the twitter api
		self.config = self._load_config(config_file)
		
		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"],
			                       self.config["CONSUMER_SECRET"])
		
		auth.set_access_token(self.config["ACCESS_TOKEN"], 
			                  self.config["ACCESS_TOKEN_SECRET"])
		
		self.api = tweepy.API(auth)
		self.bot_running = True
		self.message_queue = MessageQueue()
		self.last_checked_message = self._get_last_dm_id(self.config["LAST_ID"])
		self.receiving_commands = True
		self.verified_users = []

	def _get_last_dm_id(self, id_file):
		"""
		Retrieves the last checked dm 

		Return:
			(int) dm_id - integer ID of the last dm received
		"""

		last_dm_file = open(id_file, 'r')
		dm_id = last_dm_file.readline()
		last_dm_file.close()

		return dm_id 

	def _write_last_dm_id(self, id_file, id):
		"""
		Overwrite the last received dm id to a txt file
		
		Params:
			(int) id - ID of the last direct message checked by 
		"""

		last_dm_file = open(id_file, 'w')
		last_dm_file.write(id)
		last_dm_file.close()

		
	def _load_config(self, config_name):
		"""
		Load the bot's config file

		Return:
			(dict) config_dict - dictionary containing configuration info
		"""

		config_file = open(config_name, 'r')
		config_dict = {}

		for line in config_file:
			temp_data = line.split(':')
			config_dict[temp_data[0]] = temp_data[1].rstrip()

		config_file.close()
		return config_dict
	
	def hello_command(self):
		"""
		Return a simple hello world to the user
		"""
		return "Hello, world!"

	def about_command(self):
		"""
		Return about information about the bot
		"""
		info_list = []
		bot_info = self.api.me()

		info_list.append('Name: ' + str(bot_info.screen_name) +'\n')
		info_list.append('Desc: ' + str(bot_info.description) + '\n')
		info_list.append('Friends: ' + str(bot_info.friends_count) + '\n')
		info_list.append('Created: ' + str(bot_info.created_at) + '\n')
		info_list.append('Verified: ' + str(bot_info.verified) + '\n')
		info_list.append('URL: ' + str(bot_info.url) +'\n')
		info_list.append('Version: cenz_io-v1.0')
		
		return "".join(info_list)
	
	def eightball_command(self):
		quotes = ["It is certain",
				  "It is decidedly so",
			      "Without a doubt",
			      "Yes definitely",
			      "you may rely on it",
			      "As I see it, yes",
			      "Most likely",
			      "Outlook good",
			      "Yes",
				  "Signs point to yes",
			      "Reply hazy try again",
			      "Ask again later",
			      "Better not tell you now",
			      "Cannot predict now",
			      "Concentrate and ask again",
			      "Don't count on it",
			      "My reply is no",
			      "My sources say no",
			      "Outlook not so good",
			      "Very doubtful"]

		return quotes[randint(0, len(self.quotes))]

	def help_command(self, *args):
		"""
		Returns help commands that don't need verified users to use them
		"""
		help_dict = {"!hello":"- Returns a simple hello world!",
					 "!about":"- Returns information about the bot.",
					 "!8ball":"- Returns a accurate predictions from the magical 8ball"}
		help_string = []
		
		if len(args) == 0:
			help_string.append("Here are all the commands that I have:")
			for command_names in help_dict.keys():
				help_string.append(command_names + help_dict[command_names] + "\n")

			return "".join(help_string)
		else:
			for command in args:
				if command in help_dict:
					help_string.append(command + help_dict[command] + "\n")
				else:
					help_string.append(command + " is not a valid command\n")

			return "".join(help_string)

	def get_direct_messages(self):
		"""
		Retrieve all direct messages and throw them into the bots
		message queue

		Returns:
			A list of direct message objects
		"""
		if self.receiving_commands:
			try:
				direct_messages = self.api.direct_messages(since_id=self.last_checked_message)
				for message in direct_messages:
					self.message_queue.enqueue_node(Node(message))
					self.last_checked_message = message.id

				return direct_message
		
			except RateLimitError as e:
				print(e)
		else:
			print("Not receiving commands")
			
	def execute_commands(self):
		executed_commands = []

		try:
			while self.message_queue.get_node_count() != 0:
				current_message = self.message_queue.dequeue_node()
				command_input = ""
		except:
			pass
	def create_status(self, text):
		"""
		Update the status of the bot's twitter account

		Params:
			text - text to be used for the status of the bot

		Returns:
			Status object 
		"""
		return self.api.update_status(text)

	def send_message(self, recipient, message):
		"""
		Send a direct message from the bot to a specific recipient
		
		Params:
			recipient - The twitter id or screenname of the person to message
			message - the message to send to the recipient

		Returns:
			Direct message object
		"""
		return self.api.send_direct_message(recipient, text=message)
	
	def update_profile_image(self, filename):
		"""
		Update the bots profile picture

		Params:
			filename - the path + name of the file you'd like to change
			           the profile picture to
        
        Returns:
            Twitter User object
		"""
		return self.api.update_profile_image(filename)
	
	def shutdown(self):
		"""
		Shutdown the bot
		"""
		self._write_last_dm_id(self.config["LAST_ID"], self.last_checked_message)
		self.bot_running = False

	def add_commands(self, *commands):
		self.command_man.add_commands(*commands)

	def get_api(self):
		return self.api

	def is_running(self):
		return self.bot_running

	
