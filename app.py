from flask import Flask, render_template,redirect,Response
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import os
import requests
from pinatapy import PinataPy
from dotenv import load_dotenv
load_dotenv() 
import json
from streaming import StreamingVideoCamera,gen


# pinata_api_key='7419c5add1eb97ef8044'
# pinata_secret_api_key='339e20f14cf6d8996d4fab4a79383ef0bbb4a8b7bb58da02f408b6354de29373'
# Connect to the IPFS cloud service
# pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

proj_id = '2My7MeE7GYEYXbYCpx9BTZpYd4m'
proj_secret = 'a14627536a3deddd62467e42bf6a900b' 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'F:/VasDoc/VASDoc/static/_files/'
app.config['UPLOAD_FOLDERR'] = 'F:/VasDoc/VASDoc/static/_files/'
gateway="https://ipfs.io/ipfs/"
items = {}
dir_name = 'F:/VasDoc/VASDoc/static/_files/'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        # file.save(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']
        
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
        # result = pinata.pin_file_to_ipfs(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR']))
        # result = pinata.pin_file_to_ipfs(recent_file)
        # print(result)
        dec = json.JSONDecoder()
        i = 0
        # x = gateway+result['IpfsHash']
        # print(gateway+result['IpfsHash'])
        while i < 1:
            data, s = dec.raw_decode(response.text[i:])
            i += s + 1
            if data['Name'] == '':
                data['Name'] = 'Folder CID'
            print("%s: %s" % (data['Name'], data['Hash']))
        
        # return "<h2>Click this link{}</h2>".format(x)
            # https://VASDoc.infura-ipfs.io/ipfs/
            return redirect("https://VASDoc.infura-ipfs.io/ipfs/"+data["Hash"])
    return render_template('no-sidebar.html', form=form)


@app.route('/video', methods=['GET',"POST"])
def video():
    cam = StreamingVideoCamera()
    return Response(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug= True)