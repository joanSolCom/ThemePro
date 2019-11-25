import spacy


def process(text):
	en_nlp = spacy.load('en_core_web_sm') # TO DO
	doc = en_nlp(text)

	textConll = ""
	for sent in doc.sents:
		s = []
		sentConll = ""
		for token in sent:
			if token.text.strip():
				s.append(token.text)
				lineConll = str(token.i - sent.start + 1)+"\t"+token.text+"\t"+token.lemma_+"\t"+token.tag_+"\t"+token.dep_+"\t"+str(token.head.i - sent.start + 1)+"\n"
				sentConll+=lineConll

		textConll+=sentConll+"\n"

	return textConll

'''
path = "/home/upf/Desktop/them/transcript.txt"
txt = open(path,"r").read().strip()
#print(process(txt))
print("Conll file from Spacy parser is ready!")
'''