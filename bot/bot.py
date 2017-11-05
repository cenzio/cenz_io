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

		self.config = load_config(config_file)
		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"],
								   self.config["CONSUMER_SECRET"])

		auth.set_access_token(self.config["ACCESS_TOKEN"], 
							  self.config["ACCESS_TOKEN_SECRET"])

		#Initaliaze api, the commands, and the bot
		api = tweepy.API(auth)

		self.bot_running = True
		self.api = api

		self.commands = commands
		self.last_checked_message = 0
		self.message_queue = MessageQueue()

	def get_direct_messages(self):
		"""
		Retrieve all direct messages and throw them into the bots
		message queue
		"""
		try:
			direct_messages = self.api.direct_messages(since_id=self.last_checked_message)

			for message in direct_messages:
				self.message_queue.enqueue_node(Node(message))
				self.last_checked_message  = message.id

		except RateLimitError as e:
			print(e)
			
	def execute_commands(self):
		"""
		Reply to direct messages and execute commands
		"""
		if self.commands != None:
			try:
				while self.message_queue.get_node_count() > 0:
					current_message = self.message_queue.dequeu_node()
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
			Void
		"""
		self.api.update_status(text)

	def send_message(self, recipient, message):
		"""
		Send a direct message from the bot to a specific recipient
		
		params:
			recipient - The twitter id or screenname of the person to message
			message - the message to send to the recipient

		Returns:
			void
		"""
		self.api.send_direct_message(recipient, text=message)

	def shutdown(self):
		"""
		Shutdown the bot

		Returns:
			True if the bot shut downs gracefully
			False if the bot runs into an error shutting down
		"""
		write_last_dm_id(self.last_checked_message)
		self.bot_running = False

class BotManager(object):
	"""
	Data structure to allow multiple bots to be run in the same program
	"""
	def __init__(self, bots=None):
		self.bots = []
		
		#If there are any bots provided as a parameter 
		if bots is not None:
			for bot in bots:
				self.bots.append(bot)
