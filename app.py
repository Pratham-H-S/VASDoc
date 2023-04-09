
from flask import Flask, render_template,redirect ,request,send_file,session, url_for , g ,Response
from flask_wtf import FlaskForm
import os
import requests
from dotenv import load_dotenv
load_dotenv() 
from File_Decryption import decrypt_data
import datetime
from File_upload import File_upload
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from Verify import Verify
from wtforms.validators import InputRequired
from Decrypt_file import Decrypt
import bcrypt
from pymongo import MongoClient 
from Profile import Profile , profile
from AddReceiver import AddReceiver
from streaming import StreamingVideoCamera,gen
from mongo_files import add_files_to_mongo,get_image
# from facerecognition import gen_frames

# URL="mongodb://prajodhpragaths:Speed007@ac-9dsbmxa-shard-00-00.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-01.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-02.spncele.mongodb.net:27017/?ssl=true&replicaSet=atlas-rf01o5-shard-0&authSource=admin&retryWrites=true&w=majority"
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"
cl = MongoClient(URL)
db = cl["userdata"]
collections = db["userdata"]

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
    submit = SubmitField("Submit")

@app.before_request
def before_request():
    if "username" in session:
        g.username = session["username"]


app.register_blueprint(File_upload,url_prefix = "")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

app.register_blueprint(Decrypt,url_prefix="")
app.register_blueprint(Profile, url_prefix = "")
app.register_blueprint(Verify,url_prefix="")
app.register_blueprint(AddReceiver,url_prefix="")

@app.route('/download')
def file_download():
    file ="encrypted.txt"
    return send_file(file,as_attachment=True)

@app.route('/login',methods = ['GET','POST'])
def login():

    # users = mongo.db.users
    if "username" in session:
        return render_template("index.html")

    files = []
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        login_user = db.userdata.find_one({'name' : request.form['username']})
        if login_user:
            # if check_password_hash(request.form['password'], login_user['password']):
            if  bcrypt.checkpw(request.form['password'].encode("utf-8"),login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for("Profile.profile"))
            return "invalid user"
    return render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():

    if request.method == 'POST' :
        
        # existing_user = db.userdata.find_one({'name' : request.form['name']})
        existing_user = None
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # hashpass = generate_password_hash(request.form['password'])
            # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8') , bcrypt.gensalt())
            db.userdata.insert_one({'name' : request.form['name'] , 'password' : hashpass , 'email' : request.form['email']})
            return redirect('/login')
        else:
            print(existing_user)
            return "USer exists"
    return render_template('register.html')


@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("index"))


# @app.route('/video_register', methods=['GET',"POST"])
# def video():
#     cam = StreamingVideoCamera()
#     return Response(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

# @app.route('/facerecognition', methods=['GET',"POST"])
# def video_1():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
  app.run(host='0.0.0.0',debug= True)

























