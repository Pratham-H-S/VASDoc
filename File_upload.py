# import ipfsapi

# api = ipfsapi.connect('127.0.0.1', 5001)

# res = api.add('/1BY19CS109_FEES.pdf')

import ipfshttpclient

# Connect to the IPFS API
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5678/')

# Upload file to IPFS
res = client.add('./1BY19CS109_FEES.pdf')
hash = res['Hash']

# Print the hash of the uploaded file
print(f'Uploaded file to IPFS: {hash}')


