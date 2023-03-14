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

with open("medical_g.pdf","r") as f:
    msg = f.read()

print("Message is :",str(msg))
chunk_size = 117  # Maximum chunk size for 2048-bit key size
chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]

ciphertext = b""
for chunk in chunks:
    ciphertext += rsa.encrypt(chunk, public_key)

# encrypted_msg = rsa.encrypt(msg.encode(),public_key)

# print(msg.encode())
# print(msg.decode())



print(ciphertext)

with open("pdencrypted.txt","wb") as f:
    f.write(ciphertext)



# decrypted_msg = rsa.decrypt(encrypted_msg,private_key)

# print(decrypted_msg.decode())



# Split message into chunks


# Encrypt each chunk








