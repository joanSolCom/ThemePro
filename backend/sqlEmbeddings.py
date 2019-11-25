import pymysql.cursors
#import utils
import numpy as np
from scipy.spatial.distance import cdist
import os
from sklearn import preprocessing
import pymysql.cursors
import pymysql

class SQLEmbeddings:

	def __init__(self, dbname="Embeddings"):
		self.db = pymysql.connect(host='localhost', user='', password='', db=dbname, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	def getWordVector(self, word, tableName ="glove" ,nDims = 300):
		cursor = self.db.cursor()
		dimList = []
		for i in range(1,nDims+1):
			dimList.append("dim"+str(i))

		dims = ",".join(dimList)
		strQuery = "SELECT "+dims+" FROM "+tableName + " WHERE word='"+word+"'"
		try:
			cursor.execute(strQuery)
		except:
			return None
		vector = []

		if cursor.rowcount > 0:
			results = cursor.fetchone()
			for i in range(1,nDims+1):
				strDim = "dim"+str(i)
				dim = results[strDim]
				vector.append(float(dim))
		else:
			vector = None

		return vector

	def getMsgVector(self, msg, tableName ="glove" ,nDims = 300, lang="en"):
		cleanMsg = msg.split()
		vectors = []

		for token in cleanMsg:
			vector = self.getWordVector(token,tableName,nDims)
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
