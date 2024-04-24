import socket 
import os 
import json 
from encryption.utils import generate_keys_and_save
from encryption.hash import generate_hash,generate_signature,verify_signature
from encryption.encrypt import decrypt_data
import pandas as pd 

SERVER_PUBKEY_PATH='/home/suyash/pyaudit/src/server_configs/public_key.pem'
CLIENT_PRIVATE_PATH='/home/suyash/pyaudit/src/regular_client_configs/private_key.pem'

SERVER_IP='127.0.0.1'
SEVER_PORT=''

DATAOWNER_IP='127.0.0.1'
DATAOWNER_PORT=''

def download_file_from_server(server_host,server_port):
    
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    server_address=(server_host,server_port)

    client_socket.connect(server_address)

    tree=client_socket.recv(4096)

    print(tree.decode())
    
    file_name=input("Enter the file to download: ")
    #sending file name to download and also client ID 

    client_socket.sendall(file_name.encode())

    #Receiving file
    data_bytes=client_socket.recv(4096)
    data_str=data_bytes.decode()
    data=eval(data_str)

    file_metadata=data["file_metadata"]
    encrypted_data=data["encrypted_file"]
    signed_hash=data["signed_hash"]


    concat_data=""
    for i in range(len(file_metadata)):
        concat_data+=f"{file_metadata[i]}"
    concat_data+=f"{encrypted_data}"

    hash=generate_hash(concat_data.encode("utf-8"))
    
    flag=verify_signature(signed_hash,hash,SERVER_PUBKEY_PATH)
    print(flag)
    
    if flag:
        print('Audit sucessfull')
        client_socket.sendall('Audit sucessfull')

        print('Downloading files')
        _download_data(file_name,file_metadata,encrypted_data)
    else:
        failure_report=generate_failure_report(file_metadata)
        client_socket.sendall(str(failure_report).encode())
    

def generate_failure_report(file_metadata):

    failure_data={
        'File Name':[file_metadata[0]],
        'File version':[file_metadata[1]],
        'Failure host':[file_metadata[2][0]],
        'Failure Port':[file_metadata[2][1]]
    }

    return failure_data
    

def _download_data(file_name,file_metadata,encrypted_data):
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    file_data=decrypt_data(encrypted_data,CLIENT_PRIVATE_PATH,"suyash123@")

    file_path=os.path.join("downloads",f"{file_name}")
 
    with open(file_path,'w') as f:
        f.write(file_data.decode())

    base_file_name=os.path.splitext(file_name)[0]
    save_metadata_file_name=f".{base_file_name}.json"
    save_metadata_path=os.path.join('downloads',save_metadata_file_name)
    
    with open(save_metadata_path,'w') as f:
         json.dump(file_metadata,f) 

def _generate_keys():

    if not os.path.exists("regular_client_configs"):
        os.makedirs("regular_client_configs")
    
    private_key_path=os.path.join("regular_client_configs","private_key.pem")
    
    public_key_path=os.path.join("regular_client_configs","public_key.pem")

    password="suyash123@"

    return generate_keys_and_save(private_key_path,public_key_path,password)


def main():

    #initializing_public_key and private_key 
    download_file_from_server('127.0.0.1',51525)

if __name__=='__main__':
    main()



    

    

    
    
