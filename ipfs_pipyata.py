# download dependencies from requirements.txt
# type this command
#pip install -r requirements.txt
import os
import requests
from pinatapy import PinataPy
from dotenv import load_dotenv
load_dotenv()  
# take environment variables from .env.
#get the api keys from pinata account
pinata_api_key='7419c5add1eb97ef8044'
pinata_secret_api_key='339e20f14cf6d8996d4fab4a79383ef0bbb4a8b7bb58da02f408b6354de29373'
# Connect to the IPFS cloud service
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

# Upload the file
f = "os.pdf"
result = pinata.pin_file_to_ipfs("F:/"+f)#works even with markdown.md (text file))

# Should return the CID (unique identifier) of the file
print(result)
print(result['IpfsHash'])
# Anything waiting to be done?
print(pinata.pin_jobs())

# List of items we have pinned so far
print(pinata.pin_list())

# Total data in use
print(pinata.user_pinned_data_total())

# Get our pinned item
#gateway="https://gateway.pinata.cloud/ipfs/"
gateway="https://ipfs.io/ipfs/"
#get the file content
print(requests.get(url=gateway+result['IpfsHash']).text)
#get the link to view the file
print(gateway+result['IpfsHash'])