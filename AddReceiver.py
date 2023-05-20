from flask import Blueprint , render_template ,request,Response,session,redirect,url_for
from pymongo import MongoClient
from io import BytesIO
from bson.binary import Binary
from werkzeug.utils import secure_filename
import rsa
import gridfs
from redis_class import RedisPublish
from Crypto.PublicKey import RSA
from pycoin.ecdsa import generator_secp256k1

URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)

db = cl["receiverdata"]



AddReceiver = Blueprint("AddReceiver", __name__, static_folder= "static",template_folder="templates")

@AddReceiver.route("/AddReceiver" , methods = ['GET','POST'])

def addReceiver():
    if request.method == 'POST' :
      
        receiver = request.form['username']
        privateKey = request.form['privateKey']
        privateKey = int(privateKey)
        pubKey = (generator_secp256k1 * privateKey).pair()
        pubKey= str(pubKey)
        print(type(pubKey))
        db.receiverdata.insert_one({"from":session["username"],"to":receiver,"pubKey":pubKey})



        

        return redirect(url_for("Profile.profile"))
    return render_template("AddReceiver.html")
