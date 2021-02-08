class Node:
	
	def __init__(self, data):
		self.data = data
		self.next = None
	
	def value(self):
		return self.data

	def getNext(self):
		return self.next

	def setNext(self, newNext):
		self.next = newNext

class SLL:

	# if data_list is provided, it must be a list of values, and they are pushed one-by-one onto SLL
	def __init__(self,data_list = None):
		self.sentiNode = Node(None)
		self.endNode = self.sentiNode
		self.currentNode = self.sentiNode

		for data in data_list:
			self.push(data)

	# adds a Node with data to the front of SLL, assume data is not None
	def push(self, data):
		if data == None:
			pass

		newNode = Node(data)
		newNode.setNext(self.sentiNode.getNext())
		self.sentiNode.setNext(newNode)

	# If SLL is empty, returns None.	Else returns the data of the first Node, and removes the Node.
	def pop(self):
		if not self.sentiNode.getNext():
			return None

		popped = self.sentiNode.getNext().value()
		newHead = self.sentiNode.getNext().getNext()

		self.sentiNode.setNext(newHead)

		return popped

	# returns the data from the first Node, makes the first Node "current", else None if SLL is empty
	def getFirst(self):
		if self.sentiNode == None:
			return None

		self.currentNode = self.sentiNode.getNext()
		return self.currentNode.value()
	
	# moves internally to the Node after "current" (if possible), and returns its data, else None
	#	cannot be used after push() or pop() calls, only after getFirst() or getNext()
	def getNext(self):
		if self.currentNode == None:
			return None

		self.currentNode = self.currentNode.getNext()

		if not self.currentNode:
			return None
		else:
			return self.currentNode.value()

	# returns number of Nodes in SLL
		def length(self):
			node = getFirst()
			length = 0
		while node != None:
			node = getNext()
			length+=1

		return length

	# empties SLL, returns None
	def clear(self):
		self.sentiNode.setNext(None)
		return None

# Test...

input = [4,7,2,2,1,8]
a = SLL(input)

def forward(a):
	# use getFirst() and getNext() to acquire the list
	fwd = []
	d = a.getFirst()
	if d:
		fwd.append(d)
	d = a.getNext()
	while d:
		fwd.append(d)
		d = a.getNext()
	return fwd

def back(a):
	# use pop() to acquire the list
	bk = []
	d = a.pop()
	while d:
		bk.append(d)
		d = a.pop()
	return bk 

# Make sure that both lists are the same, and they are the reverse of the input list
fwd = forward(a)
bk = back(a)
print(fwd, bk)
if fwd == bk and fwd == input[::-1]:
	print('Success!')
else:
	print('Nope.	A problem...')
