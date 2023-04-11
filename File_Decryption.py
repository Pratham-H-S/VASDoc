import rsa
import os

# with open("encrypted.txt","rb") as f:
#     encrypted_msg = f.read()

# with open("private.pem","rb") as f:
#     private_key = rsa.PrivateKey.load_pkcs1(f.read())
dir_name = 'D:/VasDoc/static/_files/'
def decrypt_data(directory):
    files = os.listdir(directory)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    recent_file1 = files[0]
    recent_file2 = files[1]
    print("recent 1 :",recent_file1)
    print("recent 2 :",recent_file2)
    file_extension = os.path.splitext(recent_file1)[1]
    print(file_extension)
    
    if file_extension == ".txt":
        pass
    else :
        temp = recent_file2
        recent_file2 = recent_file1
        recent_file1 = temp
        
    with open(dir_name + recent_file1,"rb") as f:
        msg = f.read()
        # print(msg)

    with open(dir_name + recent_file2,"rb") as f:
        private = rsa.PrivateKey.load_pkcs1(f.read())

    decrypted_msg = rsa.decrypt(msg,private)
    return decrypted_msg.decode()

# print(decrypted_msg.decode())



