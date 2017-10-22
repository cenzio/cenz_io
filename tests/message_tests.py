import unittest
from message import MessageNode, MessageQueue

class MessageTests(unittest.TestCase):
	"""
	unit testing for our message Nodes and message Queue
	"""
	def setUp(self):
		self.message_queue = MessageQueue()

	def test_MessageNode(self):
		"""
		For testing purposes, the message node will not store Twitter messages due to
		twitters very limited api call rate. Regardless, The data the node holds is
		not as important as making sure that the data is retrievable 
		and the node is able to link to another node
		"""

		#Test the ability to retrieve data
		node = MessageNode("this is a test")
		self.assertEqual("this is a test", node.get_direct_message())
		print("node data retrieved successfully")

		#Test the ability to retrieve data number 2
		node = MessageNode("another test")
		self.assertEqual("another test", node.get_direct_message())
		print("node data retrieved successfully")

		#Test the ability to retrieve node data from a node that is linked to another node
		next_node = MessageNode("Another node")
		node.set_next_node(next_node)
		self.assertEqual(next_node.get_direct_message(), node.get_next_node().get_direct_message())
		print("Nodes linked successfully and data is able to be retrieved from the linked node")

	def test_MessageQueue(self):
		"""
		For testing purposes, the Message queue stores Message nodes in the queue. The nodes
		link to eachother and the essentially the queue just manages queueing and dequeueing or
		in simpiler terms linking and unlinking them. Like the previous test, the data stored within
		each node isn't important as making sure that the nodes work and link to eachother
		"""
		node_data = ["hello", "world", "what is up", "with you today"]
		nodes = []

		#Load the nodes
		for data in node_data:
			nodes.append(MessageNode(data))

		#queue up all the nodes
		for node in nodes:
			self.message_queue.enqueu(node)

		#Test whether the head of the queue is the correct head
		self.assertEqual(nodes[0], self.message_queue.get_head())
		print("Message queue has the correct head")

		#Test whether the tail of the queue is the correct tail
		self.assertEqual(nodes[3], self.message_queue.get_tail())
		print("Message queue has the correct tail")

		#test whether the queue dequeus all nodes in the correct order
		for i in range(len(nodes)):
			self.assertEqual(nodes[i], self.message_queue.dequeu())

if __name__ == '__main__':
	unittest.main()
