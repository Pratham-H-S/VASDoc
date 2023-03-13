import rsa

# public_key , private_key = rsa.newkeys(1024)
# Generate public key and private key 

# with open("pub.pem","wb") as f:
#     f.write(public_key.save_pkcs1("PEM"))

# with open("private.pem","wb") as f:
#     f.write(private_key.save_pkcs1("PEM")) 
# Save public and private key in pem files


with open("pub.pem" ,"rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("private.pem" ,"rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# msg = "This a message encrypted using public key"

with open("test.txt","r") as f:
    msg = f.read()

print(str(msg))

encrypted_msg = rsa.encrypt(msg.encode(),public_key)
print(str(msg))
# print(msg.encode())
# print(msg.decode())


encrypted_msg = rsa.encrypt(msg.encode(),public_key)
print(encrypted_msg)

with open("encrypted.txt","wb") as f:
    f.write(encrypted_msg)



# decrypted_msg = rsa.decrypt(encrypted_msg,private_key)

# print(decrypted_msg.decode())




