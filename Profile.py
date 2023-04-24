from flask import Flask , Blueprint , render_template , session
from pymongo import MongoClient

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db1 = cl["filedata"]
db = cl["approve_file"]


Profile = Blueprint("Profile", __name__, static_folder= "static", template_folder="template")


@Profile.route("/Profile")
def profile():
    files = []
    filehash = []
    filename =[]
    to = []
    feedback = []
    status = []
    filedata = db1.filedata.find({"from" : session['username'] })
    # found = db.approve_file.find({"received_from":session['username']})
    for f in filedata:
        
        filehash.append(f["filehash"])
        filename.append(f["filename"])
        to.append(f["to"])  
        if  f["feedback"]:
            feedback.append(f["feedback"]) 
        else:
            feedback.append("No feedback")
        if f["status"]:
            status.append(f["status"])
        else:
            status.append("unapproved")


    return render_template("Profile.html",filehash = filehash,filename = filename,to = to,feedback= feedback,status = status)