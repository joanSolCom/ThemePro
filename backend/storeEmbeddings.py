from mongoEmbeddings import MongoEmbeddings
import sys

if len(sys.argv) == 1:
    raise Exception("Need 1 param with embedding path buddy")

path = sys.argv[1]
iM = MongoEmbeddings()
iM.insertEmbeddings(path)