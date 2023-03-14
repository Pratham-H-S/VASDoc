import requests
import os
import json
from flask import Flask
proj_id = '2My7MeE7GYEYXbYCpx9BTZpYd4m'
proj_secret = 'a14627536a3deddd62467e42bf6a900b'

# make sure to use absolute path
app = Flask(__name__)
dir_name = 'F:/VasDoc/VASDoc/static/_files/'
app.config['UPLOAD_FOLDERR'] = 'F:/VasDoc/VASDoc/static/_files/'
items = {}

directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDERR'])
files = os.listdir(directory)
# files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
# recent_file = files[0]
for f in files:
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    recent_file = files[0]
    item = open(dir_name + recent_file, 'rb')
    items[f] = item
# replace above for loop with the code below for checking sub-directories
# for root, dirs, files in os.walk(dir_name):
#     for file in files:
#         filepath = root + os.sep + file
#         item = open(filepath, 'rb')
#         items[file]= item
print(items)
response = requests.post("https://ipfs.infura.io:5001/api/v0/add?pin=true&wrap-with-directory=false",
                         auth=(proj_id, proj_secret),files=items)

# for printing the CIDs in the console:
dec = json.JSONDecoder()
i = 0

while i < 1:
    data, s = dec.raw_decode(response.text[i:])
    i += s + 1
    if data['Name'] == '':
        data['Name'] = 'Folder CID'
    print("%s: %s" % (data['Name'], data['Hash']))