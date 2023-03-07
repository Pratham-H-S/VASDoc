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
pinata_api_key='b6eeff70a3db9297ee70'
pinata_secret_api_key='6d2ea1725659207d0067decbe02c2439f70b31b1f66599781d0e1fe964694e38'
# Connect to the IPFS cloud service
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)

# Upload the file
result = pinata.pin_file_to_ipfs("1BY19CS109_FEES.pdf")#works even with markdown.md (text file))

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