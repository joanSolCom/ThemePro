import numpy as np
from scipy.spatial.distance import cdist
import os
from sklearn import preprocessing
from pymongo import MongoClient

class MongoEmbeddings:

    def __init__(self, MONGOURI="mongodb://127.0.0.1:27017", embeddings="glove"):
        self.client = MongoClient(MONGOURI)
        self.db = self.client["embeddings"]
        self.embeddings = self.db[embeddings]

    def insertEmbeddings(self, path):
        f = open(path,'r')
        dictToInsert = {}
        toInsert = []
        added = []
        for idx,line in enumerate(f):
            print("Reading word number ", idx)
            splitLines = line.split()
            word = splitLines[0]
            if word not in added:
                wordEmbedding = np.array([float(value) for value in splitLines[1:]])

                dictToInsert["word"] = word
                dictToInsert["vector"] = wordEmbedding.tolist()
                toInsert.append(dictToInsert)
                added.append(word)
        
        result = None
        if toInsert:
            result = self.embeddings.insert_many(toInsert)
        
        return result


    def getWordVector(self, word):
        query = {"word":word}
        elem = self.embeddings.find_one(query)
        vector = None
        if elem:
            vector = elem["vector"]

        return vector

    def getMsgVector(self, msg, tableName ="glove"):
        cleanMsg = msg.split()
        vectors = []

        for token in cleanMsg:
            vector = self.getWordVector(token)
            if vector:
                vectors.append(vector)
        
        if vectors:
            avgVector = np.mean(vectors,axis=0)
            return avgVector.tolist()
        else:
            return None

    def aggregateVectors(self, A, B):
        C = []
        C.append(A)
        C.append(B)
        C = np.mean(C,axis=0)
        return C.tolist()

    def getNormVector(self, vector):
        return np.linalg.norm(vector)

    def distance(self, A, B, distance = "cosine"):
        return cdist([A],[B],distance)
