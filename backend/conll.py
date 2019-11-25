#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConllStruct(object):

    def __init__(self, raw_conll):
        
        self.sentences = []
        self.raw_conll = raw_conll.strip().replace("\r","")
        
        if self.raw_conll:

            raw_sentence = ""
            for line in raw_conll.split('\n'):

                if line.strip():
                    raw_sentence += line + '\n'

                elif raw_sentence:
                    sentence = ConllSentence(raw_sentence)
                    self.sentences.append(sentence)
                    raw_sentence = ""

        else:
            raise Exception('Empty conll!')

    def __iter__(self):
        return iter(self.sentences)

    def __repr__(self):
        return '\n\n'.join(map(repr, self.sentences))

class ConllSentence(object):

    def __init__(self, raw_sentence):

        self.tokens = {}
        self.token_list = []
        self.raw_sentence = raw_sentence.strip()


        if self.raw_sentence:
            self.raw_tokens = self.raw_sentence.split('\n')
            
            for raw_token in self.raw_tokens:
                token = ConllToken2009(raw_token)
                self.tokens[token.id] = token
                self.token_list.append(token)

        else:
            raise Exception('Empty conll sentence!')

    def __iter__(self):
        return iter(self.token_list)

    def __len__(self):
        return len(self.token_list)

    def __repr__(self):
        return '\n'.join(map(repr, self.token_list))

    def get_token(self, token_id):
        return self.tokens[token_id]


class ConllToken2009(object):

    def __init__(self, raw_token):

        if raw_token.strip():
            self.columns = raw_token.split('\t')

            self.id         = self.columns[0]
            self.form       = self.columns[1]
            self.lemma      = self.columns[2]
 #           self.plemma     = self.columns[2]
            self.pos        = self.columns[3]
 #           self.ppos       = self.columns[4]
 #           self.feat       = self.columns[7]
 #           self.pfeat      = self.columns[6]
            self.head       = self.columns[5]
 #           self.phead      = self.columns[8]
            self.deprel     = self.columns[4]
 #           self.pdeprel    = self.columns[10]
 #           self.fillpred   = self.columns[13]
 #           self.pred       = self.columns[12]
            if len(self.columns) > 6:
                self.them   = self.columns[6]
            else:
                self.them   = "_"
                self.columns.append(self.them)

        else:
            raise Exception('Empty conll token!')

    def __repr__(self):
        return '\t'.join([self.id, self.form, self.lemma, self.pos, self.deprel, self.head, self.them])
    

