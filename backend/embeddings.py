import numpy as np
from scipy.spatial.distance import cdist
import os
from sklearn import preprocessing

class Embeddings:

    def __init__(self, model):
        self.model = model

    def getWordVector(self, word):
        vector = None
        try:
            vector = self.model[word].tolist()
        except:
            print("unexistent word")

        return vector

    def getMsgVector(self, msg):
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
