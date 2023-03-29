from pymongo import MongoClient #import class to import mongodb
from gridfs import GridFS #import class to connect to gridfs
from bson import objectid #hello world


URL="mongodb://prajodhpragaths:Speed007@ac-9dsbmxa-shard-00-00.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-01.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-02.spncele.mongodb.net:27017/?ssl=true&replicaSet=atlas-rf01o5-shard-0&authSource=admin&retryWrites=true&w=majority"

db=MongoClient(URL)['celery']
fs=GridFS(db,"pdf")
with open("1BY19CS109_FEES.PDF") as f:
  ob=fs.put(f, content_type='application/pdf', filename='firstfile')


print(fs.get(ob).read())
