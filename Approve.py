from flask import render_template , Blueprint,request,send_file,redirect,url_for
import requests
from cryptography.fernet import Fernet
import os
from file_sign import signm
from pycoin.ecdsa import generator_secp256k1, sign
import hashlib
from pymongo import MongoClient

Approve = Blueprint("Approve" , __name__, static_folder="static" ,template_folder="templates")

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()

fernet = Fernet(key)
directory = os.getcwd()+r"\\dec_downloads\\"
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["filedata"]
db1 = cl["approve_file"]


@Approve.route('/Approve',methods = ['GET','POST'])
def approve():
    fileHash = request.args.get('fileHash')
    splitted= fileHash.split(":")
    fileHash = splitted[0]
    filename = splitted[1]
    extension = filename.split(".")
    gateway="https://VASDoc.infura-ipfs.io/ipfs/"
    data = requests.get(url=gateway+fileHash).text
    decrypted_file =  fernet.decrypt(data)
    
    with open(os.getcwd()+r"\\dec_downloads\\"+"dec."+extension[1],'wb') as f:
        f.write(decrypted_file)
    if request.method == 'POST':
        privKey = request.form['privateKey']
        privKey = int(privKey)
        print(type(privKey))
        comment = request.form['comment']
        status = request.form['Approve']
        print(status)
        # msg = 'QmcJVKBDzuSLuVu6sW7AWpBdMWu4imR6oCxWFBverWdcXw'
        msg = fileHash
        # privKey = 10723831103338713018195600
        if status == "Approve & Sign":
            msg = fileHash
            signature = signm(msg,privKey,generator_secp256k1,hashlib,sign)
            found = db.filedata.find({"filehash":fileHash})
            print(type(signature))
            print(len(signature))
            print(signature)
            signature = str(signature)
            if found:
                for f in found:
                    received_from = f["from"]
                    db1.approve_file.insert_one({"filehash":fileHash,"filename":filename,"received_from":received_from,"signature":signature,"status":"Approved","feedback":comment})
            return redirect(url_for("Profile.profile"))
        else:
            found = db.filedata.find({"filehash":fileHash})
            if found:
                for f in found:
                    received_from = f["from"]
            db1.approve_file.insert_one({"filehash":fileHash,"filename":filename,"received_from":received_from,"status":"UnApproved"})
            return redirect(url_for("Profile.profile"))


        

    
    return render_template("Approve.html")

@Approve.route('/dec_download')
def dec_download():
    f = request.args.get("file")
    print(f)
    files = os.listdir(directory)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    recent_file = files[0]
    print(recent_file)
    if f == "download":
        file = (os.getcwd()+r"\\dec_downloads\\"+recent_file)
        return send_file(file,as_attachment=True)
