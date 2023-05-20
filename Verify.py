from flask import Blueprint , render_template,request
from pymongo import MongoClient

Verify = Blueprint("Verify" , __name__, static_folder="static", template_folder="templates")

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["filedata"]
db = cl["userdata"]


@Verify.route("/Verify")

def verify():
    fileHash = request.args.get('filehash')
    print(fileHash)
    filedata = db.filedata.find_one({"filehash":fileHash})
    print(filedata)
    signature = (filedata["signature"])
    to = filedata["to"]
    print(to)
    signature = eval(signature)
    # data = db.userdata.find_one({"name"})
    print(signature)
    print(type(signature))
        

    return render_template("Verify.html")