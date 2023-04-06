
from flask import Flask , Blueprint, render_template,redirect ,request,send_file
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

File_upload = Blueprint("File_upload", __name__, static_folder="static",template_folder="template")


proj_id = '2My7MeE7GYEYXbYCpx9BTZpYd4m'
proj_secret = 'a14627536a3deddd62467e42bf6a900b' 

cl = MongoClient("mongodb://localhost:27017")
db = cl["filedata"]
db1 = cl["userdata"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'F:/VasDoc/VASDoc/static/_files/'
app.config['UPLOAD_FOLDERR'] = 'F:/VasDoc/VASDoc/static/_files/'
items = {}
dir_name = 'F:/VasDoc/VASDoc/static/_files/'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Submit")



@File_upload.route('/file_upload', methods=['GET',"POST"])
def file_upload():
    form = UploadFileForm()
    if request.method == 'POST' :
        username =  request.form['username']
        print(username)
        login_user = db1.userdata.find_one({'name' : request.form['username']})
        print(login_user)

        
        file = request.files['file'] # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
        files = os.listdir(directory)
        files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
        recent_file = files[0]
        print("this is ",recent_file)
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
            with open("public.pem","rb") as f:
                publicKey = rsa.PublicKey.load_pkcs1(f.read())
            encrypted_data = encrypt_data(data['Hash'],publicKey)
            h = data['Hash']
            if login_user:
                db.filedata.insert_one({"username" : username, "encryptedfile": encrypted_data})
                print(db)
                print("inserted")

            # https://VASDoc.infura-ipfs.io/ipfs/

        # return "<h2>Click this link{}</h2>".format(x)
            # https://VASDoc.infura-ipfs.io/ipfs/
            print(encrypted_data)
            
            # return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+x)
            return render_template('file_download.html')
    return render_template('file_upload.html', form=form)


























































# 