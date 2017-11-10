class Command(object):
	"""
	Class to represent command objeccts that can be invoked
	by dming the cenz_io bot ':' followed by the command name
	"""
	
	#Dictionary of all commands available for you
	commands = {}

	def __init__(self, command_name):
		self.command_name = '!' + command_name
		Command.commands[self.command_name] = self

	def execute(self, command_args=None):
		"""
		Execute the command
		
		Parameters:
			api - Twitter api object
			recipient - User to send the direct message to
			command_args - Arguments as list supplemented for command. Default=None
		
		Returns:
			Nothing in default implemenetation
			will return True or False signifiying that the 
			command executed properly in actual implementation
		"""
		raise NotImplementedError(self.name + 'execute function not implemented')

	
	def help(self):
		"""
		Return help information about the requested command

		Returns:
			String containing help information about command
		"""
		return "Looks like the dev didn't specify what this command does, bad dev! Let them know!"
	
	def get_name(self):
		"""
		Get the command name

		Returns:
			Command name as string
		"""
		return self.command_name

class HelloWorldCommand(Command):
	"""
	Command to greet the user with the classic
	"Hello, World!"
	"""

	def __init__(self):
		Command.__init__(self, 'hello')

	def execute(self, command_args=None):
		"""
		Send "Hello world" to the user
		"""
		return "Hello, world!"

	def help(self):
		return self.command_name + " - Returns the classic hello world message"

class AboutCommand(Command):
	"""
	Command to get information about the twitter account
	running the bot
	"""

	def __init__(self):
		Command.__init__(self, 'about')

	def execute(self, command_args=None):
		"""
		Send information about the twitter account running the
		cenz_io bot. Implmentation may change on a bot to bot basis

		Read Command for param and return info
		"""
		info_list = []
		
		info_list.append('Name: ' + str(user.screen_name) +'\n')
		info_list.append('Desc: ' + str(user.description) + '\n')
		info_list.append('Friends: ' + str(user.friends_count) + '\n')
		info_list.append('Created: ' + str(user.created_at) + '\n')
		info_list.append('Verified: ' + str(user.verified) + '\n')
		info_list.append('URL: ' + str(user.url) +'\n')
		info_list.append('Version: cenz_io-v1.0')
		
		return "".join(info_list)
		
	
	def help(self):
		"""
		Return help info about the about command
		"""
		return self.command_name + " - Returns information about the twitter account"\
			   + "Running the cenz_io bot"
		
class HelpCommand(Command):
	"""
	Sends help information to users about all/specific commands
	depending on if arguments provided by the user
	"""
	def __init__(self):
		Command.__init__(self, 'help')

	def execute(self, command_args=None):
		"""
		Get the help strings from all commands are specific commands

		Read Command for param and return info
		"""
		if command_args == None:
			all_commands_help = []
			
			for command in Command.commands:
				all_commands_help.append(command.help() + "\n")
			
			return "".join(all_commands_help)
		
		else:
			specific_commands_help = ""
			
			for command in command_args:
				if command in Command.commands:
					specific_commands_help += Command.commands[command].help() + "\n"
				else:
					specific_commands_help += command + "isn't a valid command"

			return specific_commands_help

	def help(self):
		return self.command_name + " - Returns information about commands the bot can use"

class ErrorCommand(Command):
	"""
	Called when an invalid command is called
	"""
	def __init__(self):
		Command.__init__(self, "error")

	def execute(self, command_args=None):
		return "Error, either the command you entered was invalid or something went wrong."

	def help(self):
		return self.command_name + " - Only returned when an error is run into or you've entered the wrong command"

class ShutdownCommand(Command):

	def __init__(self):
		Command.__init__(self, 'shutdown')

	def execute(self, command_args=None):
		pass

