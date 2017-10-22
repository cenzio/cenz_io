import unittest
from command import Command.commands
from bot import Bot, api

class CommandTests(unittest.TestCase):
	"""
	unit testing all of our functions 
	"""
	def setUp(self):
		self.commands = Command.commands
		self.cenz_bot = Bot(api)
		self.test_bot = Bot

	def test_Command(self):
		for command in self.commands:
			print(command)


if __name__ == '__main__':
	unittest.main()
