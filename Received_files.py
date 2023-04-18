from flask import Blueprint,render_template,Response
from receiver import connect
import redis
from redis_class import RedisSubscribe



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
    

'''
Try this too its directly using the class
'''
def recieved_files_2():
    msg=[]
    rd=RedisSubscribe('127.0.0.1',6379,"pratham")
    for i in rd.Redis_subscribe():
        msg.append(i)
    print(i)
    

