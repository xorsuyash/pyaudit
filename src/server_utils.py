import os 
import sys 
from encryption.utils import generate_keys_and_save
 

def generate_keys():

    if not os.path.exists('server_configs'):
        os.makedirs('server_configs')
    
    private_key_file_path=os.path.join('server_configs','private_key.pem')
    public_key_file_path=os.path.join('server_configs','public_key.pem')

    password="suyash123@"

    generate_keys_and_save(private_key_file_path,public_key_file_path,password)

    return private_key_file_path,public_key_file_path,password

if __name__=='__main__':
    generate_keys()