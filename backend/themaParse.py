#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
#from itertools import tee, islice, chain, izip
import sys
from conll import ConllStruct
#from syntaxStr import SyntaxStr
from utils import writeThem
from treeOperations import SyntacticTreeOperations
import operator
import collections

class ThemParser:

	def __init__(self, raw_conll):
		self.iCS = ConllStruct(raw_conll)
		self.conllParse()

	def propAnalyze(self, sentence):
		#print("Enter propAnalyze")
		#print(sentence)
		endsent = len(sentence.tokens)
		root = None
		for token in sentence:
			if token.deprel == "ROOT":
				root = token
			if int(token.id) == endsent and token.deprel == "punct":
				endsent = int(token.id) - 1
			elif int(token.id) == endsent and token.deprel != "punct":
				endsent = int(token.id)

		return root, endsent

	def thematicity(self, sentence, iTree, idnode, endsent, spcount = 1):
		begR = 1
		endT = 0
		endSP = 0
		array4level = []

		subjNode = None
		spNode = None
		splitR1 = None
		rNode = None

		nodesParent = iTree.get_children_by_parent_id(idnode)
		for n in nodesParent:
			if n.id < idnode and n.arcLabel != "punct":
				# Theme
				if n.arcLabel in ("nsubj", "nsubjpass"):
					subjNode = n
				# Frontal Spec
				elif n.arcLabel in ("cc", "prep", "advmod", "mark", "npadvmod") and n.lemma != "how":
					spNode = n
				# Frontal Rheme
				elif n.arcLabel in ("advmod","dobj") and n.pos in ("WRB", "WP"):
					splitR1 = n 
				else:
					rNode = n
					begR = int(n.id)

		if subjNode:
			#print("THEME printed", subjNode)
			minId, maxId = iTree.get_subtree_span(subjNode)
			writeThem(sentence, maxId, start= minId)
			array4level = self.form_array(array4level, minId,maxId, "T1")
			endT = maxId
			subj = minId
		if spNode:
			minId2, maxId2 = iTree.get_subtree_span(spNode)
			if (subjNode and subjNode.id > minId2) or subjNode == None:
				writeThem(sentence, maxId2, start= minId2, spcount=spcount)
				labelsp = "SP"+ str(spcount)
				array4level = self.form_array(array4level, minId2,maxId2, labelsp)
				endSP = maxId2
				spcount += 1
		if splitR1:
			minId3, maxId3 = iTree.get_subtree_span(splitR1)
			writeThem(sentence, maxId3, start= minId3, rheme= 1, level= 1)
			array4level = self.form_array(array4level, minId3,maxId3, "R1-1")
			endSP = maxId3

		# Rheme
		endR = endsent
		if endT and begR == 1:
			begR = endT + begR
		elif endSP and begR == 1:
			begR = endSP + begR

		if splitR1:
			writeThem(sentence, endR, start= begR, rheme= 1, level= 2)
			array4level = self.form_array(array4level, begR, endR, "R1-2")
		else: 
			writeThem(sentence, endR, start= begR, rheme= 1)
			array4level = self.form_array(array4level, begR, endR, "R1")

		array4level.sort(key= operator.itemgetter(0))

		return array4level

	def annot_L2_prop(self,sentence, iTree, node, prop = 1, level = 0):
		arrayL2P = []
		arrayL2T = []
		array = []

		minId, maxId = iTree.get_subtree_span(node)
		# Write P1.1
		writeThem(sentence, maxId, start= minId, prop= prop, level= level)
		lev = ".1"
		labelP = "P" + str(prop) + (lev * level)
		arrayL2P = self.form_array(arrayL2P, minId, maxId, labelP)

		#Write L2 thematicity
		arrayL2T = self.thematicity(sentence, iTree, int(node.id), maxId)

		array.append(arrayL2P)
		array.append(arrayL2T)

		return array

	def annot_L1_prop(self, sentence, iTree, coordV, root, coordP = None, prop = 1):
		#print("Entering L1 prop annot")
		minId, maxId = iTree.get_subtree_span(coordV)
		#print("NODE = ", coordV)
		#print("min max = ", minId, " ", maxId)

		arrayL1T = []
		arrayL1 = []
		arrayL2T = []

		# Theme. Check here in case there is a frontal SP for P1
		startT = 1
		endT = len(sentence.tokens) - 1
		if int(coordV.id) > int(root.id):
			#print("Entering frontal Theme")
			endT = int(coordP.id) - 1
			# Theme L1
			if coordP.arcLabel == "mark":
				writeThem(sentence, endT, start= startT)
				arrayL1T = self.form_array(arrayL1T, startT, endT, "T1")
			# P2
			prop += 1
			writeThem(sentence, endT, start= startT, prop= prop)
			arrayL1 = self.form_array(arrayL1, startT, endT, "P" + str(prop))
			# Thematicity L2
			arrayL2T = self.thematicity(sentence, iTree, int(root.id), endT)

			# Rheme L1
			if coordP.arcLabel == "mark":
				writeThem(sentence, maxId, start= minId, rheme= 1)
				arrayL1T = self.form_array(arrayL1T, minId, maxId, "R1")
			else:
				minId = minId - 1
			# P3
			prop += 1
			writeThem(sentence, maxId, start= minId, prop= prop)
			arrayL1 = self.form_array(arrayL1, minId, maxId, "P" + str(prop))
			# Thematicity L2
			## Added annotation of specifier (= coordination particle)
			if coordP.arcLabel != "mark":
				writeThem(sentence, minId, start= minId, spcount= 1)
				arrayL2T = self.form_array(arrayL2T, minId, minId, "SP1")
				arrayL2TR = self.thematicity(sentence, iTree, int(coordV.id), maxId, spcount= 2)
				arrayL2T.append(arrayL2TR[0])
			else:
				## Rest of annotation at L2
				arrayL2TR = self.thematicity(sentence, iTree, int(coordV.id), maxId, spcount= 1)
				for a in arrayL2TR:
					arrayL2T.append(a)

		# Condition for causal clauses located at the front (because x, y)
		elif int(coordV.id) < int(root.id):
			#print("Entering Frontal Rheme")
			startT = maxId + 1

			# Rheme L1
			writeThem(sentence, maxId, minId, 1)
			# P2
			prop += 1
			writeThem(sentence, maxId, start= minId, prop= prop)
			# Thematicity L2
			arrayL2T = self.thematicity(sentence, iTree, int(root.id), endT)

			# Theme L1
			writeThem(sentence, endT, start= startT)
			# P3
			prop += 1
			writeThem(sentence, endT, start= startT, prop= prop)
			# Thematicity L2
			arrayL2TR = self.thematicity(sentence, iTree, int(coordV.id), endT)
			arrayL2T.append(arrayL2TR[0])

		array1 = []
		if arrayL1T:
			array1.append(arrayL1T)
			array1.append(arrayL1)
			array1.append(arrayL2T)
		else:
			array1.append(arrayL1)
			array1.append(arrayL2T)

		return array1

	def get_type_struc(self, iTree):
		dictResult = {}

		#(self, dep1, pos2, dep3, lemma1=None)
		nodeCoord = iTree.search_same_level(dep1=["cc"],dep3=["nsubj", "nsubjpass"], pos2=["VBN", "VB", "VBD"])
		
		nodeRel = iTree.search(dependencies=["relcl"], pos= ["VBN", "VBD", "VBP", "VBZ"])

		nodeRel2 = iTree.search(pos= ["VBN", "VBD", "VBG", "VBP", "VBZ"], recursive = True, lemmaChildren = ["which", "whose", "where"])

		nodeCause = iTree.search(dependencies=["csubj","ccomp", "xcomp", "advcl", "pcomp"], pos= ["VBN", "VBD", "VBP", "VBZ"], recursive = True, lemmaChildren = ["because", "porque", "weil", "if", "si", "wenn"])

		nodeSubord = iTree.search(dependencies=["csubj","ccomp", "xcomp", "advcl", "pcomp"], pos= ["VBN", "VBD", "VBP", "VBZ"])

		# delete duplicated elements in lists
		for s in nodeSubord:
			for c in nodeCause:
				if s == c:
					nodeSubord.remove(s)

		if nodeRel and nodeRel2:
			for r in nodeRel:
				for r2 in nodeRel2:
					if r2 != r:
						nodeRel.append(r2)
					else: 
						break

		elif nodeRel2 and not nodeRel:
			nodeRel = nodeRel2

		dictResult["COORD"]= nodeCoord
		dictResult["SUBORD"]= nodeSubord
		dictResult["REL"]= nodeRel
		dictResult["CAUSE"]= nodeCause

		return dictResult


	def form_array(self, array, start, end, label):
		span = (start, end, label)
		array.append(span)

		return array

	def conllParse(self):
		new_sent = []
		array4web = []
		sentCount = 0
		self.conll = ""
		for sentence in self.iCS.sentences:
			array4sent = []
			sentCount += 1
			levelcount = 1
			propcount = 1

			root, endsent = self.propAnalyze(sentence)

			iTree = SyntacticTreeOperations(sentence.raw_sentence)

			typeStr = self.get_type_struc(iTree)

			# Sort dictionary by id of values.
			typeStr_sort = []
			keys = list(typeStr.keys())
			for k in keys:
				if not typeStr[k]:
					del typeStr[k]

			if len(typeStr) > 1:
				idVal = {}
				for t in typeStr:
					listIt = typeStr[t]
					if t == "COORD":
						firstEle = listIt[0][0]
						currId = int(firstEle.id)
						idVal[currId] = (t, listIt)						
					else:
						currId = int(listIt[0].id)
						idVal[currId] = (t, listIt)
				if idVal:
					for key,value in sorted(idVal.items()):
						typeStr_sort.append(value)

			elif len(typeStr) == 1:
				for k in typeStr:
					typeStr_sort.append((k,typeStr[k]))

			#print("============")
			#print(typeStr_sort)
			if typeStr_sort:
				for d in typeStr_sort:
					# Causal sentence. Missing particle
					if d[0] == "CAUSE":
						#print("Causal sentence found")

						arrayL1 = self.annot_L1_prop(sentence, iTree, d[1][1], root, d[1][0])
						for l in arrayL1:
							array4sent.append(l)

					# Coordination
					elif d[0] == "COORD":
						#print("Coordination found")

						for item in d[1]:
							coordV = item[1]
							coordP = item[0]
							arrayL1 = self.annot_L1_prop(sentence, iTree, coordV, root, coordP= coordP, prop= propcount)
							for l in arrayL1:
								#print(l)
								array4sent.append(l)
					# Subordination
					elif d[0] == "SUBORD" or d[0] == "REL":
						'''
						if d[0] == "REL":
							print("Relative clause found")
						else:
							print("Subordinated clause found")
						'''
						# Level 1 them
						array4level = self.thematicity(sentence, iTree, int(root.id), endsent)
						array4sent.append(array4level)
						
						for item in d[1]:
							arrayL2 = self.annot_L2_prop(sentence, iTree, item, prop= propcount, level= levelcount)
							levelcount += 1

							for a in arrayL2:
								array4sent.append(a)
			else:
				#print("SIMPLE")
				# Level 1 them
				array4level = self.thematicity(sentence, iTree, int(root.id), endsent)
				array4sent.append(array4level)


			array4web.append(array4sent)
			self.conll += str(sentence) + "\n"

		self.levels = array4web

		#print("ARRAY FOR WEB")
		#print(array4web)

'''
			tokens = []
			# Code for printing CONLL output
			for token in sentence:
				tokens.append(str(token))

			tokens= "\n".join(tokens)
			new_sent.append(tokens)

		new_conll = "\n\n".join(new_sent)
#		print(new_conll)
		result = open(path + "output.conll", "w")
		result.write(new_conll)
		result.close()
		print("New conll has been printed")
'''

if __name__ == '__main__':
	path = "/home/upf/Desktop/docs/themaParse/"
	pathIn = "/home/upf/Desktop/docs/themaParse/test/complexSent.conll"
	# cd Desktop/de && python mod1_synt2them.py out_eval.conll eval_them.conll
	#path = sys.argv[1]

	iT = ThemParser(path, pathIn)
