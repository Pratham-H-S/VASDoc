from flask import Blueprint,render_template,Response,session
from pymongo import MongoClient



Received_files = Blueprint("received_files",__name__,static_folder="static",template_folder="templates")
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["filedata"]

@Received_files.route("/Received_files")

def received_files():
    found = db.filedata.find({'to':session['username']})
    received_from = []
    file_hash = []
    file_name = []
    if found:
        for f in found:
            file_hash.append(f["filehash"])
            file_name.append(f["filename"])
            received_from.append(f["from"])            
    else:
        return "No data"
    
    return render_template("Received_files.html",file_hash=file_hash,file_name = file_name,received_from= received_from,zip=zip)

        
    


    

