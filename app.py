from flask import Flask, render_template,redirect
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

pinata_api_key='7419c5add1eb97ef8044'
pinata_secret_api_key='339e20f14cf6d8996d4fab4a79383ef0bbb4a8b7bb58da02f408b6354de29373'
# Connect to the IPFS cloud service
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ''
app.config['UPLOAD_FOLDERR'] = ''
gateway="https://ipfs.io/ipfs/"

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
        # result = pinata.pin_file_to_ipfs(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR']))
        result = pinata.pin_file_to_ipfs(recent_file)
        print(result)
        x = gateway+result['IpfsHash']
        print(gateway+result['IpfsHash'])
        
        # return "<h2>Click this link{}</h2>".format(x)
        return redirect("https://ipfs.io/ipfs/"+result["IpfsHash"])
    return render_template('no-sidebar.html', form=form)

# def file_Upload():
#   if request.method == 'POST':
#     file = request.files['file']
#     return "File uploaded !!"
#   else:
#     return render_template("no-sidebar.html")



if __name__ == '__main__':
  app.run(host='0.0.0.0',debug= True)