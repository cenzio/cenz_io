"""
Module for running the cenz_io multifunctional twitter bot
"""
import tweepy
from tweepy import TweepError, RateLimitError

import time

from random import randint
from bot.message import MessageNode, MessageQueue

class TwitterBot(object):
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
			(dict) config: Contains configuration settings for the bot
			(bool) debug_mode: Whether the bot is in debug mode or not
			(API) api: Tweepy API object
			(User) me: Twitter user object of the bot profile
			(int) last_checked_message: id of the last dm received
			(bool) receiving commands: whether the bot is receiving commands or not

		"""

		self.bot_running = True
		self.config = self._load_config(config_file)
		

		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"],
			                       self.config["CONSUMER_SECRET"])
		
		auth.set_access_token(self.config["ACCESS_TOKEN"], 
			                  self.config["ACCESS_TOKEN_SECRET"])
		
		#setup debug mode if set to true in config
		if self.config["DEBUG_MODE"] == "True":
			self.debug_mode = True
		else:
			self.debug_mode = False


		self.api = tweepy.API(auth)
		self.me = self.api.me()
		self.message_queue = MessageQueue()
		
		#Setup command_mode if set to True in config
		if self.config["COMMAND_MODE"] == "True":
			self.command_mode = True
			self.last_checked_message = self._get_last_dm_id()
			self.verified_users = ["xC3NZ"]
		else:
			self.command_mode = False

		self._print_info("Debug mode set to true")
		self._print_info("Config is up")
		self._print_info("tweepy API and bot identity setup")
		self._print_info("command_mode is:" + str(self.command_mode))
		self._print_info("verified_users are:" + ",".join(self.verified_users))

	def _get_last_dm_id(self):
		"""
		Retrieves the last checked dm 

		Return:
			(int) dm_id - integer ID of the last dm received
		"""
		self._print_info("Getting last direct message ID")
		
		last_dm_file = open(self.config["ID_FILE"], 'r')
		dm_id = last_dm_file.readline()
		last_dm_file.close()
		
		self._print_info("Last DM received from " + self.config["ID_FILE"] + " With an ID of " + str(dm_id))
		
		return dm_id 

	def _write_last_dm_id(self, id):
		"""
		Overwrite the last received dm id to a txt file
		
		Params:
			(int) id - ID of the last direct message checked by 
		"""
		self._print_info("Writing the last dm received to file")
		
		last_dm_file = open(self.config["ID_FILE"], 'w')
		last_dm_file.write(id)
		last_dm_file.close()
		
		self._print_info("Finished writing dm id to " + self.config["ID_FILE"])
		
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

	def _print_info(self, message):
		"""
		Print info if debug mode is on
		"""
		if self.debug_mode:
			print("[" + self.me.screen_name + "]" + "[INFO]" + message)
	
	def _print_error(self, message):
		"""
		print errors if debug mode is on
		"""
		if self.debug_mode:
			print("[" + self.me.screen_name + "]" + "[ERROR]" + message)

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
		"""
		Return a quote from the magical 8ball
		"""
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
		Returns information on how to use non privileged bot commands
		"""
		help_dict = {"!hello":" - Returns a simple hello world!",
					 "!about":" - Returns information about the bot.",
					 "!8ball":" - Returns a accurate predictions from the magical 8ball"}
		
		help_string = []
		
		if len(args) == 0:
			help_string.append("Here are all the commands that I have:\n")
			
			for command in help_dict.keys():
				help_string.append(command+ help_dict[command] + "\n")

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
			(list)direct_messages: A list of direct message objects received from the bot
		"""
		if self.command_mode:
			try:
				direct_messages = self.api.direct_messages(since_id=self.last_checked_message)
				
				for message in direct_messages:
					self.message_queue.enqueue_node(Node(message))
					self.last_checked_message = message.id
					self._print_info("Message from '" + message.screen_name + "' with message '" + message.text + "' received.")
				
				return direct_messages
		
			except RateLimitError as rate:
				self._print_error(rate)
		else:
			print("Not receiving commands")
			
	def execute_commands(self):
		"""
		Execute commands sent to the bot from a user

		Returns:
			(list)executed_commands: list of Message twitter objects sent by the bot
		"""
		executed_commands = []

		try:
			
			while self.message_queue.get_node_count() != 0:
				current_message = self.message_queue.dequeue_node()
				user = current_message.screen_name
				
				user_message = current_message.text.split()
				command = user_message[0].lower()
				command_output = ""

				if not command_input[0].startswith('!'):
					command_output = "I'm sorry, I only accept commands, which start with ! :("
				else:
					if command == "!help":
						command_output =  self.help_command(user_message[1:])
					elif command == "!hello":
						command_output = self.hello_command()
					elif command == "!8ball":
						command_output = self.eightball_command()
					elif command == "!about":
						command_output = self.about_command()
					else:
						command_output = "Sorry, I do not have that have command or you mispelled it :("

				executed_commands.append(self.send_message(user, command_output))

			return executed_commands

		except RateLimitError as rate:
			self._print_error(rate)
			return executed_commands

	def create_status(self, text):
		"""
		Update the status of the bot's twitter account

		Params:
			text - text to be used for the status of the bot

		Returns:
			Status object 
		"""
		self._print_info("Posting status:" + text)
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
		self._print_info("Sending message to:" + recipient + "containing the text")
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
		self._print_info("Updated prorfile picture")
		return self.api.update_profile_image(filename)
	
	def get_api(self):
		return self.api

	def get_me(self):
		return self.me

	def is_running(self):
		return self.bot_running

	def shutdown(self):
		"""
		Shutdown the bot
		"""
		self._write_last_dm_id(self.config["LAST_ID"], self.last_checked_message)
		self.bot_running = False
		self._print_info("Bot is now shutting down")
