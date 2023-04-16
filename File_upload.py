
from flask import Flask , Blueprint, render_template,redirect ,request,send_file,session,url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import json
from File_Encryption import encrypt_data
import rsa
from File_Decryption import decrypt_data
import requests
from wtforms.validators import InputRequired
from pymongo import MongoClient
from redis_class import RedisPublish
from cryptography.fernet import Fernet

# key = Fernet.generate_key()

# with open('mykey.key', 'wb') as mykey:
#     mykey.write(key)

File_upload = Blueprint("File_upload", __name__, static_folder="static",template_folder="template")

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()




fernet = Fernet(key)

proj_id = '2My7MeE7GYEYXbYCpx9BTZpYd4m'
proj_secret = 'a14627536a3deddd62467e42bf6a900b' 
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["filedata"]
db1 = cl["userdata"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '42jk3234kjhsejfirewoiofh32jfk'
app.config['UPLOAD_FOLDER'] = (os.getcwd()+r"\\static\\_files\\")
app.config['UPLOAD_FOLDERR'] = (os.getcwd()+r"\\static\\_files\\")
items = {}
dir_name = (os.getcwd()+r"\\static\\_files\\")



class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Submit")



@File_upload.route('/file_upload', methods=['GET',"POST"])
def file_upload():
    form = UploadFileForm()
    if request.method == 'POST' :
        # username =  request.form['options[]']
        username = request.form.getlist('options[]')       
        login_user = db1.userdata.find_one({'name' : session['username']})
        
        file = request.files['file'] # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
        files = os.listdir(directory)
        files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
        recent_file = files[0]
        print("this is ",recent_file)
        with open(dir_name + recent_file,"rb") as f:
            data = f.read()
        encrypted_file = fernet.encrypt(data)
        with open(dir_name + recent_file,"wb") as f:
            f.write(encrypted_file)
        for f in files:
            files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
            recent_file = files[0]
            item = open(dir_name + recent_file, 'rb')
            items[f] = item
        response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=true&wrap-with-directory=false",
                         auth=(proj_id, proj_secret),files=items)
        # print(result)
        dec = json.JSONDecoder()
        i = 0
        while i < 1:
            data, s = dec.raw_decode(response.text[i:])
            i += s + 1
            if data['Name'] == '':
                data['Name'] = 'Folder CID'
            print("%s: %s" % (data['Name'], data['Hash']))
            x = data["Hash"]
            if login_user:
                for i in username:
                    connect=RedisPublish('127.0.0.1',6379,i)
                    connect.Redis_publish(json.dumps({i:x}))
                    
                db.filedata.insert_one({"username" : username, "filehash": x,"filename" : file.filename})
                print(db)
                print("inserted")

            # https://VASDoc.infura-ipfs.io/ipfs/

        # return "<h2>Click this link{}</h2>".format(x)
            # https://VASDoc.infura-ipfs.io/ipfs/

            
            gateway="https://VASDoc.infura-ipfs.io/ipfs/"
            print(requests.get(url=gateway+data['Hash']).text)
            data = requests.get(url=gateway+data['Hash']).text
            decrypted_file =  fernet.decrypt(data)
            with open("dec.pdf","wb") as f:
                f.write(decrypted_file)

            
            # return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+x)
            return redirect(url_for("Profile.profile"))
    return render_template('file_upload.html', form=form)


























































# 