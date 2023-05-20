from pymongo import MongoClient #import class to import mongodb
from gridfs import GridFS #import class to connect to gridfs
from bson import objectid #hello world
import os
import cv2

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"
db=MongoClient(URL)['images']
fs=GridFS(db)
def add_files_to_mongo(username):
  for i in range(10):
      os.chdir(os.getcwd()+"\images")
      file = username+str(i+1)+".jpg"
      with open(file, 'rb') as f:
          contents = f.read()
      fs.put(contents, filename=username+str(i+1))
      os.remove(file)
      os.chdir(os.getcwd()+'\..')

    


def delete_all():
  db.fs.files.delete_many({})


def get_img(username):
  data=db.fs.files.find_one({'filename':username+"1"})
  my_id=data['_id']
  output_file=fs.get(my_id).read()
  file=open(os.getcwd()+r"\\image.jpg",'wb')
  file.write(output_file)
  file.close()
  return output_file

def get_image():
  data=db.fs.files.find({})
  j=1
  for i in data:
      print(i)
      my_id=i['_id']
      filename=i['filename']
      output_file=fs.get(my_id).read()
      file=open(os.getcwd()+r"\\images_from_mongo_training\\"+str(filename)+"_image"+str(j)+".jpg",'wb')
      file.write(output_file)
      file.close()
      j+=1

def delete_imges_in_folder():
   for dirpath,dirname,filenames in os.walk(os.getcwd()+r'\\images_from_mongo_training\\'):
      for f in filenames:
         os.remove(dirpath+r"\\"+f)

# import json
# def read():
#     with open(os.getcwd()+r"\\name.json", "r") as outfile:
#                         print(json.load(outfile))


# get_image()
# delete_imges_in_folder()
# delete_all()
