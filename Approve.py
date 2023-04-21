from flask import render_template , Blueprint,request,send_file
import requests
from cryptography.fernet import Fernet
import os

Approve = Blueprint("Approve" , __name__, static_folder="static" ,template_folder="templates")

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()

fernet = Fernet(key)
directory = os.getcwd()+r"\\dec_downloads\\"

@Approve.route('/Approve')


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
