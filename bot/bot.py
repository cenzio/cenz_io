"""
Module for running the cenz_io multifunctional twitter bot
"""
import tweepy
import time
from base_commands import Command
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, AUTHORIZED_USERS
from utils import get_last_dm_id, write_last_dm_id

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#Initaliaze api, the commands, and the bot
api = tweepy.API(auth)

class Bot(object):
	"""
	Twitter bot that will be used to receive and act on commands
	You can create multiple bots if you'd like but there is no support
	for running multiple bots at the same time within the same program
	"""

	def __init__(self, api, commands):
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
		self.bot_running = True
		self.api = api
		self.commands = commands
		self.message_queue = MessageQueue
		self.last_checked_message = get_last_dm_id()

	def get_direct_messages(self):
		try:
			direct_messages = self.api.direct_messages(since_id=self.last_checked_message)
		except Exception as e:
			print(e)

	def run(self):

		while self.bot_running:
			print('Fetching dms... ' sep='')
			direct_messages = self.api.direct_messages(since_id=since_id)
		
			if len(direct_messages) > 1:
				self.last_checked_message = direct_messages[0].id
			else:
				time.sleep(3)
				continue

			for dm in direct_messages:
				
				command_text = dm.text.split()
				command_name = command_text[0].lower()
				
				try:
					if command_name in commands:
						if len(command_text[1:]) > 0:
							self.commands[command_name].execute(self.api, dm.sender.screen_name, command_args=command_text[1:])
						else:
							self.commands[command_name].execute(self.api, dm.sender.screen_name)
					else:
						self.commands[':error'].execute(self.api, dm.sender.screen_name)
				
				except Exception as e:
					print(e)

			print('Fetched!')
			time.sleep(1)

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

class BotManager(object):
	"""
	Data structure to allow multiple bots to be run in the same program
	"""
	def __init__(self, bots=None):
		self.bots = []
		
		#If there are any bots that are not none
		if bots is not None:
			for bot in bots:
				self.bots.append(bot)




if __name__ == "__main__":
	cenz_io = Bot(api, Command.commands)
	cenz_io.run()
