from pycoin.ecdsa import generator_secp256k1, sign, verify
import hashlib, secrets
from PIL import Image
from redis_class import RedisPublish
import json
from flask import Blueprint ,session ,render_template
from mongo_files import get_img
import chardet
from pymongo import MongoClient
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["userdata"]

GenKeys = Blueprint("GenKeys",__name__,static_folder="static",template_folder="templates") 
@GenKeys.route("/genKeys")

def genKeys():
  j = get_img(session['username'])
  
  print(j)
  val = 0
  for i in range(0,len(j)):
    if type(i) is int:
      val += i

  print(val)

  privKey = secrets.randbelow(10**14)
  
  privKey = privKey * 116 * val
  print("Private key :",privKey)
  with open("private.txt","w") as f:
    f.write(str(privKey))

  pubKey = (generator_secp256k1 * privKey).pair()
  print(pubKey)
  pubKey = str(pubKey)
  db.userdata.find_one_and_update({'name': session['username']}, {"$set":{"pubKey":pubKey}})

  return render_template("file_download.html")

# print("Public key: (" + hex(pubKey[0]) + ", " + hex(pubKey[1]) + ")")

