
from flask import Flask, render_template,redirect ,request,send_file,session, url_for , g ,Response
from flask_wtf import FlaskForm
import os
import time
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
from mongo_files import add_files_to_mongo,get_image,delete_imges_in_folder,get_img
from GenKeys import GenKeys
import cv2
import face_recognition
import cv2
import face_recognition
import numpy as np
import os
from Received_files import Received_files

# from facerecognition import gen_frames
#URL="mongodb://prajodhpragaths:Speed007@ac-9dsbmxa-shard-00-00.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-01.spncele.mongodb.net:27017,ac-9dsbmxa-shard-00-02.spncele.mongodb.net:27017/?ssl=true&replicaSet=atlas-rf01o5-shard-0&authSource=admin&retryWrites=true&w=majority"
URL = "mongodb+srv://vasdoc:vasdoc123@cluster0.1ssyf7f.mongodb.net/test"

cl = MongoClient(URL)
db = cl["userdata"]
collections = db["userdata"]
username=""

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
app.register_blueprint(GenKeys,url_prefix="")
app.register_blueprint(Received_files,url_prefix ="")

@app.route('/download')
def file_download():
    file ="private.txt"
    return send_file(file,as_attachment=True)

@app.route('/login',methods = ['GET','POST'])
def login():
    # users = mongo.db.users
    if "username" in session:
        return render_template("index.html")
    if request.method=="POST" and request.form.get("face") is not None and 'username' in request.form:
            session['messages'] =  request.form['username'] 
            return redirect('/face_recognition')

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
            session['messages'] =  request.form['name'] 
            session['username'] = request.form['name']
            
            return redirect('/video')
        else:
            print(existing_user)
            return "USer exists"
    return render_template('register.html')


@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("index"))

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_register', methods=['GET',"POST"])
def video_registeration():
    username = session['messages']
    cam = StreamingVideoCamera(username)
    return Response(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")



'''
face recognition
'''
def set_up(known_face_encodings,known_face_names):
    delete_imges_in_folder()
    get_image()

    for dirpath,dirname,filenames in os.walk(os.getcwd()+r'\\images_from_mongo_training\\'):
        for f in filenames:
            if int(f.split("image")[-1].split(".")[0])%10==0:
                image = face_recognition.load_image_file("images_from_mongo_training\\"+f)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(str(f.split(".")[0][:-2]))

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


    

def gen_frames(camera,known_face_names,known_face_encodings):  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/face_recognition')
def video_feed():
    camera = cv2.VideoCapture(0)
    known_face_encodings=[]
    known_face_names=[]
    set_up(known_face_encodings,known_face_names)
    return Response(gen_frames(camera,known_face_names,known_face_encodings), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
  app.run(host='0.0.0.0',debug= True)

























