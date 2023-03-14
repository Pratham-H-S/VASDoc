import rsa 

with open("pub.pem","rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("sign.txt" ,"rb") as f:
    signed_text = f.read()

with open("test.txt","r") as f:
    msg = f.read()

verified = rsa.verify(msg.encode(),signed_text,public_key)

if verified == "SHA-256":
    print("verification success")
else:
    print("error")