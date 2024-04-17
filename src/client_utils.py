import os 
import shutil 
from encryption.utils import generate_keys_and_save
from encryption.encrypt import encrypt_data
from encryption.hash import generate_hash,generate_signature


def generate_client_cache(file_path,n):
    
    if not os.path.exists('client_cache'):
        os.makedirs('client_cache')
    
    file_name=os.path.basename(file_path)

    file_dict={}
    for i in range(1,n+1):

        copy_file_name=f"{file_name}_{i}"
        copy_file_path=os.path.join('client_cache',copy_file_name)
        shutil.copyfile(file_path,copy_file_path)
        file_dict[copy_file_name]=copy_file_path

    return file_dict

def generate_keys():

    if not os.path.exists('client_configs'):
        os.makedirs('client_configs')
    
    private_key_file_path=os.path.join('client_cache','private_key.pem')
    public_key_file_path=os.path.join('client_configs','public_key.pem')

    password="suyash123@"

    generate_keys_and_save(private_key_file_path,public_key_file_path,password)

    return private_key_file_path,public_key_file_path,password

def generate_encrypted_data(file_path,public_key_path):
    
    with open(file_path,"r") as file:
        file_data=file.read()

    enc_data=encrypt_data(file_data.encode("utf-8"),public_key_path)

    return enc_data

def create_signature(data,private_key_path,password):
     
    hash=generate_hash(data.encode("utf-8"))

    signature=generate_signature(hash,private_key_path,password)

    return signature
