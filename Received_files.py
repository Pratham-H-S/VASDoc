from flask import Blueprint,render_template,Response
from receiver import connect
import redis




Received_files = Blueprint("received_files",__name__,static_folder="static",template_folder="templates")

@Received_files.route("/Received_files")

def received_files():
    msg=[]
    for i in connect():
        msg.append(i)
    if msg is None:
        return Response("No data")
    else:
        return render_template("Received_files.html",msg = msg)

