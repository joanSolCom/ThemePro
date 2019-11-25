from __future__ import division
import codecs
from pprint import pprint

class Tree:

	def __init__(self, rootNode, nodeDict={}):
		self.nodeDict = nodeDict
		self.root = rootNode

		if self.root:
			if not self.root.id in self.nodeDict:
				self.nodeDict[self.root.id] = rootNode

	def getDepthIterator(self, initNode = None):
		
		if not initNode:
			initNode = self.root
		
		stack = []
		stack.append(initNode)

		while stack:
			current = stack.pop(0)
			if current:
				yield current
				for child in current.children:
					stack.insert(0,child)

	def getWidthIterator(self, initNode = None):
		
		if not initNode:
			initNode = self.root

		queue = []
		queue.append(initNode)

		while queue:
			current = queue.pop()
			if current:
				yield current
				for child in current.children:
					queue.insert(0,child)


	def __str__(self):
		strRepr = ""
		
		queue = []
		queue.append(self.root)
		strRepr += "ROOT-> "+ str(self.root.id) + "\n"
		i = 1
		while queue:
			current = queue.pop()
			strRepr += "CHILDREN OF "+str(current.id)+" -> "
			for child in current.children:
				strRepr += str(child.id) + "\t"
				queue.insert(0,child)
	
			strRepr +="\n"
			i+=1

		return strRepr

class Node:

	def __init__(self, meta, idNode, arcLabel, parentId):
		self.meta = meta
		self.children = []
		self.parent = parentId
		self.id = idNode
		self.arcLabel = arcLabel

	def setParent(self, parentNode):
		self.parent = parentNode

	def addChild(self, childNode):
		self.children.append(childNode)

	def __str__(self):
		strRepr = ""
		strRepr += self.id + " " + self.meta + " " + self.arcLabel
		return strRepr


class SyntacticNode(Node):

	def __init__(self, meta, idNode, arcLabel, parentId):
		self.meta = meta
		self.children = []
		self.parent = parentId
		self.id = idNode
		self.arcLabel = arcLabel

		pieces = meta.split("\t")
		self.word = pieces[1]
		self.lemma = pieces[2]
		self.pos = pieces[3]
		self.parentid = parentId

	def __str__(self):
		strRepr = ""
		strRepr += str(self.id) + " " + self.word + " " +self.lemma + " "+ self.pos + " " + str(self.parentid) + " " + self.arcLabel
		return strRepr

	def __repr__(self):
		strRepr = ""
		strRepr += str(self.id) + " " + self.word + " " +self.lemma + " "+ self.pos + " " + str(self.parentid) + " " + self.arcLabel
		return strRepr

class DiscourseNode(Node):

	def __init__(self, idNode=None, parentNode=None, meta="", arcLabel="", nucleous="", label=""):

		self.id = idNode
		self.parent = parentNode
		self.meta = meta
		self.arcLabel = arcLabel
		self.nucleous = nucleous
		self.label = label
		self.children = []
		
	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.id) + " " + self.arcLabel + " " + self.nucleous + " " + self.meta
