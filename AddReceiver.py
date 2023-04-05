from flask import Blueprint , render_template ,request,Response
from pymongo import MongoClient
from io import BytesIO
from bson.binary import Binary
from werkzeug.utils import secure_filename
import rsa
import gridfs
from Crypto.PublicKey import RSA

cl = MongoClient("mongodb://localhost:27017")
db = cl["filedata"]
fs = gridfs.GridFS(db)


AddReceiver = Blueprint("AddReceiver", __name__, static_folder= "static",template_folder="templates")

@AddReceiver.route("/AddReceiver" , methods = ['GET','POST'])

def addReceiver():
    if request.method == 'POST' :
        f = request.files['file']
        filename = secure_filename(f.filename)
        x = f.stream.read()
        # f.seek(0)
        # print(f.read())
        # x = f.read()
        print(x)
        with open("pub.pem","wb") as fb:
            fb.write(x)
        with open("pub.pem","rb") as fb:
            data = (fb.read())
        print(data)
        d = data
        fs.put(d,filename = f.filename)
        db.filedata.insert_one({"username" : request.form['username'], "public": d})
        filedata = db.filedata.find({"username":"bv"})
        for f in filedata:
            pubkey = f["public"]
        print(type(pubkey))
        with open("pubkey.pem","wb") as f:
            f.write(pubkey)
        with open("pub.pem","rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        file = fs.find_one({'filename': 'public.pem'})
        # file_data = BytesIO(file.read())
        # file_data.seek(0)
        file_data= file["key_pem"]
        p_key = RSA.import_key(file_data) 
        with open("pu.pem","wb") as f:
            f.write(p_key.save_pkcs1("PEM"))
        print(file_data)
        # return Response(file_data, content_type=file.content_type)
        # with open("pub.pem","rb") as f:
        #     public_key = rsa.PublicKey.load_pkcs1(f.read())
        # k = b""
        # k = file_data
        # print(k)
        # msg = "sfsdfsdfsdfsdfsfsdsdf32423rdsfsdf"
        # encrypted_msg = rsa.encrypt(msg.encode(),k)
        # with open("encrypted.txt" , "wb") as f:
        #     f.write(encrypted_msg)
        return render_template("AddReceiver.html")
    return render_template("AddReceiver.html")
