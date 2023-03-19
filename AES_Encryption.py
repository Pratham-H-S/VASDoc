from Crypto.Random import get_random_bytes
from  Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad

simple_key = get_random_bytes(32)
salt = simple_key
password = "kk123"
key = PBKDF2(password,salt,dkLen=32)
print(key)
with open("1BY19CS109_FEES.pdf","rb") as f:
    msg = f.read()

cipher = AES.new(key, AES.MODE_CBC)
print(cipher)
ciphered_data = cipher.encrypt(pad(msg,AES.block_size))
# print(ciphered_data)

with open("encrypted.bin" ,"wb") as f :
    f.write(cipher.iv) # Creates  a binary fog 
    f.write(ciphered_data)

with open("encrypted.bin","rb") as f:
    iv = f.read(16)
    decrypt_data = f.read()

cipher = AES.new(key,AES.MODE_CBC,iv = iv)
original = unpad(cipher.decrypt(decrypt_data),AES.block_size)

with open("decrypted.pdf","wb") as f:
    f.write(original)
