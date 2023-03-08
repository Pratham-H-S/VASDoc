import rsa

with open("encrypted.txt","rb") as f:
    encrypted_msg = f.read()

with open("private.pem","rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


decrypted_msg = rsa.decrypt(encrypted_msg,private_key)

print(decrypted_msg.decode())

