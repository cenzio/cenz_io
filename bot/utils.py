"""
Modules containing utils that for retrieving info for the bots
"""

def get_last_dm_id(id_file):
	"""
	Retrieves the last checked dm 
	"""

	#Open the file for reading, read the id, and then close it
	last_dm_file = open(id_file, 'r')
	id = last_dm_file.readline()
	last_dm_file.close()

	return id 

def write_last_dm_id(id_file, id):
	"""
	Overwrite the last received dm id to a txt file
	
	Params:
		id - ID of the last direct message checked by 
	"""

	last_dm_file = open(id_file, 'w')
	last_dm_file.write(id)
	last_dm_file.close()


def load_config(config_name):
	"""
	Load the bot's config file
	"""
	config_file = open(config_name, 'r')
	config_dict = {}
	for line in config_file:
		temp_data = line.split(':')
		config_dict[temp_data[0]] = temp_data[1].rstrip()

	config_file.close()
	return config_dict
		