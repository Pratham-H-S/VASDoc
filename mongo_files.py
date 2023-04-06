from pymongo import MongoClient #import class to import mongodb
from gridfs import GridFS #import class to connect to gridfs
from bson import objectid #hello world
import os
import cv2

URL="mongodb://prajodhpragaths:Speed007@ac-9dsbmxa-shard-00-00.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-01.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-02.spncele.mongodb.net:27017/?ssl=true&replicaSet=atlas-rf01o5-shard-0&authSource=admin&retryWrites=true&w=majority"
db=MongoClient(URL)['epochs']
fs=GridFS(db)
def add_files_to_mongo():
  for i in range(10):
      os.chdir(os.getcwd()+"\images")
      file = "data"+str(i+1)+".jpg"
      with open(file, 'rb') as f:
          contents = f.read()
      fs.put(contents, filename="file"+str(i+1))
      os.remove(file)
      os.chdir(os.getcwd()+'\..')
    


def delete_all():
  db.fs.files.delete_many({})


def get_image():
  data=db.fs.files.find_one({'filename':"file1"})
  my_id=data['_id']
  output_file=fs.get(my_id).read()
  file=open(r"\Users\prajo\Desktop\ipfs\VASDoc\image.jpg",'wb')
  file.write(output_file)
  file.close()
# print(output_file)
