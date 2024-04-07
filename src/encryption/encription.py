import json 
import secrets 
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes 
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import serialization, hashes ,hmac
from cryptography.hazmat.primitives.asymmetric import rsa,padding 



secret_key=secrets.token_bytes(32)

with open('file1.txt','rb') as file:
    file_data=file.read()

digest=hashes.Hash(hashes.SHA256())
digest.update(file_data)
file_hash=digest.finalize()

#Encript the file 
backend=default_backend()
cipher=Cipher(algorithms.AES(secret_key),modes.GCM(None),backend=backend)
encryptor=cipher.encryptor()
encripted_file=encryptor.update(file_data)+encryptor.finalize()


# Load private key and sign hash 
with open('private_key.pem','rb') as key_file:
    private_key=serialization.load_pem_private_key(
        key_file.read(),
        password=None 
    )

signature=private_key.sign(file_hash,padding.PKCS1v15(),hashes.SHA256())


data_dict={
    'file_id':'123456',
    'time_stamp':'something',
    'encrypted_file':encripted_file,
    'signed_hash':signature,
    'secret_key':secret_key
}

with open("do_creds.json",'w') as f:
    json.dump(data_dict,f)