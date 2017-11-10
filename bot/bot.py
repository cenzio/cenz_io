"""
Module for running the cenz_io multifunctional twitter bot
"""
import tweepy
from tweepy import TweepError, RateLimitError
import time


from bot.base_commands import Command
from bot.utils import get_last_dm_id, write_last_dm_id, load_config
from bot.message import MessageNode, MessageQueue


class Bot(object):
	"""
	Twitter bot that will be used to receive and act on commands
	You can create multiple bots if you'd like but there is no support
	for running multiple bots at the same time within the same program
	"""

	def __init__(self, config_file, commands=None):
		"""
		Params:
			api: the tweepy api for the specific user you want to link the bot to
			commands: dictionary that contains commands you want the bot to be able to use
		
		Variables:
			bot_running: Whether the bot is active and running or not
			api: the tweepy api
			commands: the commands available to the user
			last_checked_message: id of the last dm received
		"""

		#Authenticate with the twitter api
		self.config = load_config(config_file)
		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"],
								   self.config["CONSUMER_SECRET"])
		auth.set_access_token(self.config["ACCESS_TOKEN"], 
							  self.config["ACCESS_TOKEN_SECRET"])
		

		self.api = tweepy.API(auth)
		self.bot_running = True
		self.commands = commands
		self.message_queue = MessageQueue()
		self.last_checked_message = get_last_dm_id(self.config["LAST_ID"])

	def is_running(self):
		return self.bot_running

	def get_direct_messages(self):
		"""
		Retrieve all direct messages and throw them into the bots
		message queue

		Returns:
			A list of direct message objects
		"""
		try:
			direct_messages = self.api.direct_messages(since_id=self.last_checked_message)
			for message in direct_messages:
				self.message_queue.enqueue_node(Node(message))
				self.last_checked_message = message.id

			return direct_message
		except RateLimitError as e:
			print(e)
			
	def execute_commands(self):
		"""
		Reply to direct message commands if there are any of the message
		queue

		Returns:
			list of Direct message objects that were replied to
		"""
		if self.commands != None:
			messages_sent = []
			try:
				while self.message_queue.get_node_count() > 0:
					current_message = self.message_queue.dequeu_node()
					command = current_message.text.split()
					command_output = ""

					#Execute command if available
					if command[0] in self.commands and len(command[1:]) > 0:
						command_output = commands[command[0]].execute(commands[1:])
					elif command[0] in self.commands and len(command[1:]) < 0:
						command_output = commands[command[0]].execute()
					else:	
						command_output = commands['!error'].execute()

					messages_sent.append(current_message)

				return messages_sent
			
			except RateLimitError as e:
				print(e)
		else:
			print("This bot doesn't have any commands to execute")

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
		write_last_dm_id(self.config["LAST_ID"], self.last_checked_message)
		self.bot_running = False
