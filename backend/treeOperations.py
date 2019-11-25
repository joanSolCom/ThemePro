from tree import Node, SyntacticNode, DiscourseNode, Tree
import codecs

class TreeOperations:

	def __init__(self, conllStringSentence):
		conllStringSentence = conllStringSentence.strip()
		if not conllStringSentence:
			raise ValueError("Please input a correct conll sentence")
			return
		self.tree = self.conll_to_tree(conllStringSentence)

	def conll_to_tree(self, conllString):
		conllArray = conllString.split("\n")
		nodes, root = self.create_nodes(conllArray)
		self.link_nodes(nodes)
		return Tree(root, nodes)

	def create_nodes(self, conllArray):
		nodeDict = {}
		root = None
		for line in conllArray:
			pieces = line.split("\t")
			idNode = int(pieces[0])
			arcLabel = pieces[4]
			parentId = int(pieces[5])
			iNode = Node(line, idNode, arcLabel, parentId)
			nodeDict[idNode] = iNode
			if parentId == idNode:
				root = iNode

		return nodeDict, root


	def link_nodes(self, nodeDict):
		for idNode, iNode in nodeDict.items():
			if iNode.parent != iNode.id:
				iParent = nodeDict[iNode.parent]
				iParent.addChild(iNode)
				iNode.setParent(iParent)

	
	def get_ramification_factor(self, initNode = None):
		if initNode:
			it = self.tree.getWidthIterator(initNode)
		else:
			it = self.tree.getWidthIterator()

		acumChilds = 0
		levels = 1
		for current in it:
			nchilds = len(current.children)
			if nchilds > 0:
				acumChilds+=nchilds
				levels+=1

		return acumChilds / levels

	def get_max_width(self, initNode = None):
		it = self.tree.getWidthIterator(initNode)
		maxWidth = 0

		for current in it:
			nchilds = len(current.children)
			if nchilds > maxWidth:
				maxWidth = nchilds

		return maxWidth

	def get_max_depth(self, initNode = None):
		if not initNode:
			initNode = self.tree.root

		return self.get_max_depth_recursive(initNode)


	def get_max_depth_recursive(self, node):
		depth = []

		if node:
			if not node.children:
				return 0
		if not node:
			return 0
		
		for child in node.children:
			depth.append(self.get_max_depth_recursive(child))

		return 1 + max(depth)

	def get_node_depth(self, node):
		current = node
		depth = 0
		while current.parent:
			depth+=1
			current = current.parent
		return depth

class SyntacticTreeOperations(TreeOperations):

	'''
		Gets the maximum width and depth below a node that has a given relation 
		with its father. EX: For every subordinate clause, we get the maximum value
		of width and depth of the subtree BELOW the node which has a SUB relation with its father.
	'''
	def get_relation_width_depth(self, relation):
		
		it = self.tree.getWidthIterator()
		widthDepths = []

		for current in it:
			if current.arcLabel == relation:
				width = self.get_max_width(current)
				depth = self.get_max_depth(current)
				widthDepths.append((width,depth))

		return widthDepths

	def get_relation_depth_level(self, relation):
		it = self.tree.getWidthIterator()
		levels = []
		for current in it:
			if current.arcLabel == relation:
				level = self.get_node_depth(current)
				levels.append(level)

		return levels

	def get_relation_ramification_factor(self, relation):
		it = self.tree.getWidthIterator()
		ramFactors = []
		for current in it:
			if current.arcLabel == relation:
				ramFactor = self.get_ramification_factor(current)
				ramFactors.append(ramFactor)

		return ramFactors

	def search_deps_frequency(self, searchedRels = []):

		it = self.tree.getWidthIterator()
		relFreq = {}
		searchAll = False
		if not searchedRels:
			searchAll = True

		total = 0
		for current in it:
			if current:
				for child in current.children:
					if child.arcLabel in searchedRels or searchAll:
						if child.arcLabel in relFreq:
							relFreq[child.arcLabel] +=1
						else:
							relFreq[child.arcLabel] =1
						total+=1

		return relFreq, total

	def search_dep_nodes(self, dependency):
		it = self.tree.getWidthIterator()
		nodes = []
		for current in it:
			if current:
				for child in current.children:
					if child.arcLabel == dependency:
						nodes.append(child)

		return nodes

	def search_same_level(self, dep1, pos2, dep3, lemma1=None):
		it = self.tree.getWidthIterator()
		nodes = []
		for current in it:
			if current:
				firstNode = None
				secondNode = None
				for child in current.children:					
					if child.arcLabel in dep1 or (lemma1 and child.lemma in lemma1):
						firstNode = child
					if child.pos in pos2:
						secondNode = child
				
				if firstNode and secondNode:
					if self.searchChild(dependencies=["nsubj","nsubjpass"], startNode=secondNode):
						nodes.append((firstNode,secondNode))

		return nodes

	def searchChild(self, dependencies, startNode):
		for child in startNode.children:
			if child.arcLabel in dependencies:
				return True

		return False


	def search(self, dependencies = [], pos = [], lemmas = [], startNode = None, recursive=False, depChildren=[], posChildren=[], lemmaChildren=[]):
		it = None
		if not startNode:
			it = self.tree.getWidthIterator()
		else:
			it = self.tree.getWidthIterator(startNode)

		nodes = []
		for current in it:
			if current:
				for child in current.children:
					if dependencies and pos and lemmas:
						if child.arcLabel in dependencies and child.pos in pos and child.lemma in lemmas:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)
					elif dependencies and pos and not lemmas:
						if child.arcLabel in dependencies and child.pos in pos:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.extend(nodesChildren)
									nodes.append(child)
							else:
								nodes.append(child)
					elif dependencies and lemmas and not pos:
						if child.arcLabel in dependencies and child.lemma in lemmas:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)
					elif pos and lemmas and not dependencies:
						if child.lemma in lemmas and child.pos in pos:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)
					elif pos and not lemmas and not dependencies:
						if child.pos in pos:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)
					elif lemmas and not pos and not dependencies:
						if child.lemma in lemmas:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)
					elif dependencies and not lemmas and not pos:
						if child.arcLabel in dependencies:
							if recursive:
								nodesChildren = self.search(depChildren, posChildren, lemmaChildren, child, False)
								if nodesChildren:
									nodes.append(child)
							else:
								nodes.append(child)

		return nodes

	def get_prev_same_level_nodes(self, dependency):
		it = self.tree.getWidthIterator()
		nodes = []
		mainNodeIds = []
		for current in it:
			if current:
				nodeLevel = []
				found = False
				for child in current.children:
					if child.arcLabel != "punct":
						nodeLevel.append(child)
						if child.arcLabel == dependency:
							found = True
							nodeLevel.pop()
							mainNodeIds.append(child.id)

				if found:
					nodes.append(nodeLevel)

		i = 0
		filteredNodes = []
		while i < len(nodes):
			refId = mainNodeIds[i]
			filteredSubList = []
			for node in nodes[i]:
				if node.id < refId:
					filteredSubList.append(node)

			filteredNodes.append(filteredSubList)
			i+=1

		return filteredNodes

	def get_subtree_span(self, initNode):
		it = self.tree.getWidthIterator(initNode)
		minId = initNode.id
		maxId = initNode.id
		for current in it:
			if current:	
				for child in current.children:
					#print("CHILD ID "+str(child.id))
					if child.id < minId:
						minId = child.id
					if child.id > maxId:
						maxId = child.id
						if child.arcLabel == "punct":
							maxId -= 1

		return minId, maxId

	def get_children_by_parent_id(self, idParent):
		it = self.tree.getWidthIterator()
		children = []
		for current in it:
			#print current
			if current and current.id == idParent:
				children = current.children
				break

		return children

	def search_pos_frequency(self, searchedPos = []):
		it = self.tree.getWidthIterator()
		posFreq = {}

		searchAll = False
		if not searchedPos:
			searchAll = True

		total = 0
		for current in it:
			if current:
				for child in current.children:
					if child.pos in searchedPos or searchAll:
						if child.pos in posFreq:
							posFreq[child.pos] +=1
						else:
							posFreq[child.pos] =1
						total+=1

		return posFreq, total

	def get_composed_verb_ratio(self):
		verbTags = ["VB","VBD","VBG","VBN","VBP","VBZ", "MD"]
		verbFreq, total = self.search_pos_frequency(verbTags)
		depFreq, vcFreq = self.search_deps_frequency(["VC"])

		if vcFreq > 0 and total > 0:
			composedVerbRatio = vcFreq / total
		else:
			composedVerbRatio = 0.0

		return composedVerbRatio

	def get_modal_ratio(self):
		verbTags = ["VB","VBD","VBG","VBN","VBP","VBZ", "MD"]
		verbFreq, total = self.search_pos_frequency(verbTags)

		if total > 0 and "MD" in verbFreq:
			modalRatio = verbFreq["MD"]/ total
		else:
			modalRatio = 0.0

		return modalRatio

	def create_nodes(self, conllArray):
		
		nodeDict = {}
		root = None
		for line in conllArray:
			pieces = line.split("\t")
			idNode = int(pieces[0])
			arcLabel = pieces[4]
			parentId = int(pieces[5])

			iNode = SyntacticNode(line, idNode, arcLabel, parentId)
			nodeDict[idNode] = iNode
			if parentId == idNode:
				root = iNode

		return nodeDict, root

class DiscourseTreeOperations(SyntacticTreeOperations):

	def __init__(self, discourseString):
        
		lines = discourseString.split("\n") 
		lines[0] = lines[0][5:]
		root = self.createNode(lines, 0, None)
		tree = Tree(root)
		self.addChildren(tree, root, 2, lines, 1)
		self.tree = tree

	def createNode(self,lines, idx, parent):
		line = lines[idx].strip()
		node = DiscourseNode(idx, parent)
		if line.startswith("TEXT:"):
			node.arcLabel, node.meta = line.split(":", 1)
		else:
			pieces = line.split(" ", 1)
			if len(pieces) == 1:
				node.arcLabel = pieces[0]
			else:
				node.arcLabel, node.nucleous = pieces

		return node

	def addChildren(self,tree, parent, level, lines, idx):
		spaces = level
		while idx < len(lines) and spaces >= level:
			spaces = len(lines[idx]) - len(lines[idx].lstrip(" "))

			if spaces > level:
				idx = self.addChildren(tree, node, spaces, lines, idx)

			elif spaces == level:
				node = self.createNode(lines, idx, parent)
				parent.children.append(node)
				tree.nodeDict[node.id] = node

				idx += 1

		return idx


if __name__ == "__main__":

	path = "/home/joan/Escritorio/Datasets/englishDataset/discourse/71_male"
	discText = codecs.open(path,"r",encoding="utf-8").read()
	iDisc = DiscourseTreeOperations(discText)
	'''path = "/home/joan/Escritorio/conlls/8855_female_connl_parsed.conll"

	conllString = codecs.open(path,"r",encoding="utf-8").read()
	conllSents = conllString.split("\n\n")
	
	adverbialRelations = ["ADV","TMP","LOC","DIR","MNR","PRP","EXT"]
	modifierRelations = ["NMOD","PMOD","AMOD"]

	verbTags = ["VB","VBD","VBG","VBN","VBP","VBZ", "MD"]
	nounTags = ["NN","NNS","NNP","NNPS"]
	adverbTags = ["RB","RBR","RBS","WRB"]
	adjectiveTags = ["JJ","JJR","JJS"]
	pronounTags = ["PRP","PRP$","WP","WP$"]
	determinerTags = ["DT","PDT","WDT"]
	conjunctionTags = ["CC","IN"]

	superlatives = ["JJS","RBS"]
	comparatives = ["JJR","RBR"]
	
	pastVerbs = ["VBD","VBN"]
	presentVerbs = ["VBG","VBP","VBZ"]


	for conllSent in conllSents:
		
		try:
			iTree = SyntacticTreeOperations(conllSent)		
			print "SUB "
			widthDepth = iTree.get_relation_width_depth("SUB")
			ramFactors = iTree.get_relation_ramification_factor("SUB")
			levels = iTree.get_relation_depth_level("SUB")
			print str(widthDepth)
			print str(ramFactors)
			print str(levels)
			print "------------------"
			print "COORD "
			widthDepth = iTree.get_relation_width_depth("COORD")
			ramFactors = iTree.get_relation_ramification_factor("COORD")
			levels = iTree.get_relation_depth_level("COORD")
			print str(widthDepth)
			print str(ramFactors)
			print str(levels)
			print "_________________"
			relFreq = iTree.search_deps_frequency(adverbialRelations)
			print "ADVERBIAL TAG FREQ",relFreq
			posFreq, total = iTree.search_pos_frequency()
			print posFreq, total

			ramFact = iTree.get_ramification_factor()
			print ramFact
			width = iTree.get_max_width()
			print "width -> " + str(width)
			depth = iTree.get_max_depth()
			print "depth -> " + str(depth)
			
			composedVerbRatio = iTree.get_composed_verb_ratio()
			print composedVerbRatio
			modalRatio = iTree.get_modal_ratio()
			print modalRatio

		except ValueError:
			print "Empty Sentence, skipping "
			continue
	'''
