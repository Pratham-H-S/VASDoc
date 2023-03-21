from flask import Flask,Blueprint , render_template,request,redirect
from werkzeug.utils import secure_filename
import os
from File_Encryption import encrypt_data
from File_Decryption import decrypt_data
from File_Decryption import decrypt_data
import datetime

Decrypt = Blueprint("Decrypt",__name__,static_folder="static",template_folder="templates")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'F:/VasDoc/VASDoc/static/_files/'
app.config['UPLOAD_FOLDERR'] = 'F:/VasDoc/VASDoc/static/_files/'
items = {}
dir_name = 'F:/VasDoc/VASDoc/static/_files/'

@Decrypt.route('/decrypt_file',methods=['GET',"POST"])
def decrypt_file():    
    if request.method == 'POST':
        file = request.files['file_name1']
        # print(file.stream.read())
        x = b""
        x = file.stream.read()
        x.decode()
        print(x)
        
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename))
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename), "wb") as f:
            f.write(x)
        
        file = request.files['file_name2']
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M"+"611")
        new_filename = f"{timestamp}_{filename}"
        
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],new_filename))
        
        directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
        data = (decrypt_data(directory))
        print(data)  
             
        return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+data)
    return  render_template("decrypt_file.html")