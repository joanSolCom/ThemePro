#!/usr/bin/env python
# -*- coding: utf-8 -*-

import constants

def writeLabel(word, label, level = 0):
	if word.them == constants.EMPTY:
		word.them = label
	elif label == word.them:
		word.them = word.them
	elif word.them[0] in (constants.OPEN_T, constants.OPEN_P):
		word.them += label
	else:
		word.them = label + word.them


def buildLabel(word, span, oneword = 0, count = 1, level = 0):
	if oneword and level:
		label = constants.OPEN_T + span + str(count) + constants.DASH + str(level) + constants.CLOSE_T
		writeLabel(word, label)
	elif oneword:
		label = constants.OPEN_T + span + str(count) + constants.CLOSE_T
		writeLabel(word, label)

	elif span in ("[", "{"):
		writeLabel(word, span)

	elif span == "R" and level:
		labelsplitR = constants.CLOSE_T + span + str(count) + constants.DASH + str(level)
		writeLabel(word, labelsplitR)

	elif span != "P":
		labelT = constants.CLOSE_T + span + str(count)
		writeLabel(word, labelT)

	elif level:
		lev = ".1"
		labelP = constants.CLOSE_P + span + str(count) + (lev * level)
		writeLabel(word, labelP, level)

	else:
		labelP = constants.CLOSE_P + span + str(count)
		writeLabel(word, labelP)

def writeThem(sentence, end, start = 1, rheme = 0, spcount = 0, prop = 0, level = 0):
	if rheme and end != start:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_T)
		if level:
			buildLabel(sentence.tokens[str(end)], constants.RHEME, count= 1, level= level)
		else:
			buildLabel(sentence.tokens[str(end)], constants.RHEME)
	# single word thematicity T or SP
	elif end == start and prop == 0:
		if spcount == 0 and rheme == 0:
			buildLabel(sentence.tokens[str(end)], constants.THEME, oneword= 1)
		elif rheme:
			buildLabel(sentence.tokens[str(end)], constants.RHEME, oneword= 1, count= 1, level= level)
		else:
			buildLabel(sentence.tokens[str(end)], constants.SPEC, oneword= 1, count= spcount)

	# multi word T or SP
	elif end != start and prop == 0 and rheme == 0:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_T)
		if spcount == 0:
			buildLabel(sentence.tokens[str(end)], constants.THEME)

		else:
			buildLabel(sentence.tokens[str(end)], constants.SPEC, count= spcount)

	elif level:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_P)
		buildLabel(sentence.tokens[str(end)], constants.PROP, count= prop, level= level)

	elif prop:
		buildLabel(sentence.tokens[str(start)], constants.OPEN_P)
		buildLabel(sentence.tokens[str(end)], constants.PROP, count= prop)
