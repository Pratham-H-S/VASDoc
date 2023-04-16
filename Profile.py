from flask import Flask , Blueprint , render_template , session
from pymongo import MongoClient

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db1 = cl["filedata"]


Profile = Blueprint("Profile", __name__, static_folder= "static", template_folder="template")


@Profile.route("/Profile")
def profile():
    files = []
    filedata = db1.filedata.find({"username" : session['username'] })
    for f in filedata:
        files.append(f["filehash"])
    return render_template("Profile.html",files=files)