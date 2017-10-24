
class MessageNode(object):
	"""
	Nodes to represent all twitter direct messages that have not been responded to by the bot
	
	"""
	def __init__(self, direct_message):
		"""
		Params:
			direct_message: DirectMessage object 
		"""
		self.direct_message = direct_message
		self.next_node = None

	def set_next_node(self, next_node):
		self.next_node = next_node

	def get_next_node(self):
		return self.next_node

	def get_direct_message(self):
		return self.direct_message

class MessageQueue(object):
	"""
	Message queue for the twitter bot to queue tweets to respond to
	"""
	def __init__(self):
		"""
		Params:
			None
		Variables instantiated:
			head: Head node of the queue (first in the queue)
			tail: tail node of the queue (last in the queue)
			node_count: the amount of nodes in the queue
		"""
		self.head = None
		self.tail = None
		self.node_count = 0

	def enqueue_node(self, message_node):
		"""
		add a direct message node to the queue

		Params:
			message_node: Message node containing a DirectMessage object
		
		Returns:
			Void
		"""
		if self.head == None:
			self.head = message_node
			self.tail = self.head
		else:
			self.tail.set_next_node(message_node)
			self.tail = self.tail.get_next_node()

		self.node_count += 1

	def dequeue_node(self):
		"""
		Dequeue the MessageQueue if there are any message nodes in it

		Params:
			None

		Returns:
			The first MessageNode in the queue
		"""
		return_node = None

		if self.head == None:
			print("The queue is empty!")
		else:
			return_node = self.head
			self.head = self.head.get_next_node() 
			self.node_count -= 1

			return return_node.get_direct_message()

	
	def get_head(self):
		return self.head

	def get_tail(self):
		return self.tail

	def get_node_count(self):
		return self.node_count

