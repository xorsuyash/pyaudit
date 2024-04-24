import socket 
import os 
from encryption.utils import generate_keys_and_save
from encryption.hash import generate_hash,generate_signature,verify_signature
from encryption.encrypt import decrypt_data


SERVER_IP='127.0.0.1'
SEVER_PORT=''

DATAOWNER_IP='127.0.0.1'
DATAOWNER_PORT=''

def download_file_from_server(file_name,server_host,server_port):
    
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    server_address=(server_host,server_port)

    client_socket.connect(server_address)

    tree=client_socket.recv(4096)

    print(tree.decode())
    
    file_name=input("Enter the file to download: ")
    #sending file name to download and also client ID 

    client_socket.sendall(file_name.encode())

    #Receiving file

    data=client_socket.recv(4096)
    
    return data



def _generate_keys():

    if not os.path.exists("regular_client_configs"):
        os.makedirs("regular_client_configs")
    
    private_key_path=os.path.join("regular_client_configs","private_key.pem")
    
    public_key_path=os.path.join("regular_client_configs","public_key.pem")

    password="suyash123@"

    return generate_keys_and_save(private_key_path,public_key_path,password)


def main():

    #initializing_public_key and private_key 
    private_key_path,public_key_path=_generate_keys()

    

    

    
    
