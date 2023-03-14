import rsa

with open("private.pem" , "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# msg = "This file is signed using private key and verified using public key"

with open("test.txt","r") as f:
    msg = f.read()

signed_file = rsa.sign(msg.encode(),private_key,"SHA-256")

print(signed_file)

with open("sign.txt","wb") as f:
    f.write(signed_file)
