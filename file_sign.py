

from pycoin.ecdsa import generator_secp256k1, sign
import hashlib

# msg = 'QmcJVKBDzuSLuVu6sW7AWpBdMWu4imR6oCxWFBverWdcXw'

# privKey = 345678909876543456789765434567896543456789

def signm(msg,privKey,generator_secp256k1,hashlib,sign):
  
  hashBytes = hashlib.sha3_256(msg.encode("utf8")).digest()
  hashBytes= int.from_bytes(hashBytes, byteorder="big")  
  signature = sign(generator_secp256k1, privKey, hashBytes)
  return signature
  
  
# print(signm(msg,privKey,generator_secp256k1,hashlib,sign))























