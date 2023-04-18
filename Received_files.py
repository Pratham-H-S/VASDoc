from flask import Blueprint,render_template,Response
from receiver import connect
import redis
from redis_class import RedisSubscribe



Received_files = Blueprint("received_files",__name__,static_folder="static",template_folder="templates")

@Received_files.route("/Received_files")

def received_files():
    msg=[]
    connection=redis.Redis('127.0.0.1',6379,decode_responses=True)
    subscriber=connection.pubsub()
    subscriber.subscribe("pratham")
    for message in subscriber.listen():
            msg.append(message)
    if msg is None:
        return Response("No data")
    else:
        return render_template("Received_files.html",msg = msg)

@Received_files.route("/Received_files1")
def received_files_modified():
    def streaming_response():
        connection=redis.Redis('127.0.0.1',6379)
        subscriber=connection.pubsub()
        subscriber.subscribe("pratham")
        for message in subscriber.listen():
                yield "data: {}\n\n".format(message)
    return Response(streaming_response(),mimetype="text/event-stream")

'''
Try this too its directly using the class
'''
def recieved_files_2():
    msg=[]
    rd=RedisSubscribe('127.0.0.1',6379,"pratham")
    for i in rd.Redis_subscribe():
        msg.append(i)
    print(i)
    

