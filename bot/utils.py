"""
Modules containing utils that for retrieving info for the bots
"""

def get_last_dm_id():
	"""
	Retrieves the last checked dm 

	Returns:
		integer id of the last checked dm
	"""

	#Open the file for reading, read the id, and then close it
	last_dm_file = open('data/last.txt', 'r')
	id = last_dm_file.readline()
	last_dm_file.close()

	return id 

def write_last_dm_id(id):
	"""
	Overwrite the last received dm id to a txt file
	
	Params:
		id - ID of the last direct message checked by 

	Returns:
		Nothing
	"""

	#Open the file, write the id, and then close it
	last_dm_file = open('data/last.txt', 'w')
	last_dm_file.write(id)
	last_dm_file.close()