from OpenSSL import crypto

# Generate a new private key
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)
# key.generate_key(crypto.TYPE_RSA, 2048, '-rand', 'joi.jpeg')

# Create a self-signed X.509 certificate containing the public key
cert = crypto.X509()
cert.set_pubkey(key)
cert.sign(key, "sha256")

# Save the private key and certificate to files
with open("private_key.pem", "wb") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

with open("public_key.pem", "wb") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))


# import os
# from OpenSSL import crypto

# # Read data from an image file to generate a seed value
# with open("joi.jpeg", "rb") as f:
#     image_data = f.read()
# rand_seed = sum(bytearray(image_data))  # calculate a seed value from the image data

# # Generate a sequence of random bytes and add them to the OpenSSL random number generator
# rand_bytes = os.urandom(1024)  # generate a sequence of 1024 random bytes
# crypto._lib.RAND_seed(rand_bytes, len(rand_bytes))  # add the random bytes to the OpenSSL random number generator

# # Generate a new private key
# key = crypto.PKey()
# key.generate_key(crypto.TYPE_RSA, 2048)

# # Create a self-signed X.509 certificate containing the public key
# cert = crypto.X509()
# cert.set_pubkey(key)
# cert.sign(key, "sha256")

# # Save the private key and certificate to files
# with open("private_key.pem", "wb") as f:
#     f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
# with open("public_key.pem", "wb") as f:
#     f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
