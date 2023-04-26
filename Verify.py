from flask import Blueprint , render_template,request
from pymongo import MongoClient
from check_sign import verifym
from pycoin.ecdsa import generator_secp256k1, sign, verify
import hashlib, secrets


Verify = Blueprint("Verify" , __name__, static_folder="static", template_folder="templates")

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["filedata"]
db1 = cl["userdata"]


@Verify.route("/Verify")

def verify_file():
    fileHash = request.args.get('filehash')
    print(type(fileHash))
    print(fileHash)
    filedata = db.filedata.find({"filehash":fileHash})
    print(filedata)
    for f in filedata:
        signature = (f["signature"])
        to = f["to"]
    print(signature)
    signature = eval(signature)
    print(type(signature))
    pub = db1.userdata.find({"name" : to})
    for f in pub:
        pubKey = (f["pubKey"])
    pubKey = eval(pubKey)
    print(type(pubKey))
    print(pubKey)

    valid = verifym(fileHash,pubKey,generator_secp256k1,hashlib,signature,verify)
    # hashBytes = hashlib.sha3_256(fileHash.encode("utf8")).digest()
    # hashBytes =  int.from_bytes(hashBytes, byteorder="big")
    # validated =  verify(generator_secp256k1, pubKey, fileHash, signature)
    # print(validated)
    print(valid)
    if valid:
        message = "Valid Document Signed by\t"+to
        return render_template("Verify.html",message = message)
    else:
        message = "Invalid Document"
        return render_template("Verify.html",message = message)

        

    return render_template("Verify.html")