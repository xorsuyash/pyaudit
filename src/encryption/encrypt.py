from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend

def encrypt_data(data, public_key_path):

    with open(public_key_path,"rb") as key_file:
         public_key_bytes=key_file.read()
    
    public_key=load_pem_public_key(
         public_key_bytes,
         backend=default_backend()
    )
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def decrypt_data(encrypted_data, private_key_path,password):
    
    
    with open(private_key_path, "rb") as key_file:
            private_key_bytes = key_file.read()

    private_key = load_pem_private_key(
    private_key_bytes,
    password=password.encode() if password else None,
    backend=default_backend()
        )
    
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

if __name__=="__main__":
     
     from utils import generate_keys_and_save
     password="suyash123@"
     
     #generate_keys_and_save("private_key.pem","public_key.pem",password)

     with open("file1.txt","r") as f:
          file_data=f.read()
    
     encrypted_data=encrypt_data(file_data.encode("utf-8"),"public_key.pem")
     decrypted_data=decrypt_data(encrypted_data,"private_key.pem",password)


     print(decrypted_data)