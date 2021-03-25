from pymongo import MongoClient
MONGOURI="mongodb://127.0.0.1:27017"
client = MongoClient(MONGOURI)
db = client.embeddings
coll = db.glove
resp = coll.create_index([ ("word", -1) ])

print("index response:", resp)
print("Created database and index")

