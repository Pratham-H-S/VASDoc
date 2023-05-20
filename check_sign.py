from pycoin.ecdsa import generator_secp256k1, sign, verify
import hashlib, secrets

def  verifym(msg,pubKey,generator_secp256k1,hashlib,signature,verify):
  hashBytes = hashlib.sha3_256(msg.encode("utf8")).digest()
  hashBytes =  int.from_bytes(hashBytes, byteorder="big")
  validated =  verify(generator_secp256k1, pubKey, hashBytes, signature)
  return validated