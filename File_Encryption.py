
import rsa

# public_key ,private_key = rsa.newkeys(2048)

# # print(public_key)

# with open("public.pem","wb") as f:
#     f.write(public_key.save_pkcs1("PEM"))

# with open("private.pem","wb") as f:
#     f.write(private_key.save_pkcs1("PEM"))

# with open("1BY19CS109_FEES.pdf","rb") as f:
#     msg = f.read()

# with open("public.pem","rb") as f:
#     public_key = rsa.PublicKey.load_pkcs1(f.read())

# with open("private.pem","rb") as f:
#     private_key = rsa.PrivateKey.load_pkcs1(f.read())

# encrypted_msg = rsa.encrypt(msg,public_key)

# with open("encrypted.txt" , "wb") as f:
#     f.write(encrypted_msg)


def encrypt_data(msg,public_key):
    k = b""
    k = public_key
    encrypted_msg = rsa.encrypt(msg.encode(),k)
    with open("encrypted.txt" , "wb") as f:
        f.write(encrypted_msg)
    return encrypted_msg
 





