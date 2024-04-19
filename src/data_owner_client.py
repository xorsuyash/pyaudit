from client_utils import generate_client_cache,generate_keys,generate_encrypted_data,create_signature
from encryption.hash import verify_signature
from encryption.hash import generate_hash
import yaml 
import socket  
import os 
import shutil


SERVER_LIST_PATH="/home/suyash/pyaudit/src/client_configs/hosts.yaml"
SERVER_PUBKEY_PATH="/home/suyash/pyaudit/src/server_configs/public_key.pem"

def send_data_to_server(server_host,server_port,data):

    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    client_socket.connect((server_host,server_port))

    client_socket.sendall(str(data).encode())
    
    #getting response from the server
    ack = client_socket.recv(4096)
    
    return ack


def _load_server_list(server_list_path):

    with open(server_list_path) as yaml_file:
        config_data=yaml.safe_load(yaml_file)
    
    server_list=[]
    for server_name,server_info in config_data['ServerList'].items():
        server_list.append((server_info['host'],server_info['port']))
    
    return server_list



def prepare_data_to_send(file_path,server_list,no_server,server_pubkey_path):

    file_dict=generate_client_cache(file_path,no_server)

    private_key_path,public_key_path,password=generate_keys()
    
    #creating file metadata 
    file_names=[names for names in file_dict.keys()]
    file_metadata={}
    file_version="1xdc"
    for i in range(len(server_list)):
        data_list=[]
        data_list.append(file_names[i])
        data_list.append(file_version)
        data_list.append(server_list[i])
        file_metadata[file_names[i]]=data_list
    
    #generating encrypted data 
    encryption_dict={}
    for file_name,file_path in file_dict.items():
        
        enc_data=generate_encrypted_data(file_path,server_pubkey_path)
        encryption_dict[file_name]=enc_data 
    
    #generating signatures 
    signature_dict={}
    hash_dict={}
    
    concat_data_list=[]
    for file_list in file_metadata.values():
        concatenated_metadata=""
        for i in range(len(file_list)):
            concatenated_metadata+=f"{file_list[i]}"
        concat_data_list.append(concatenated_metadata)
    
    encryption_list=[encryption for encryption in encryption_dict.values()]
    
    #reading file 
    file_paths=[path for path in file_dict.values()]
    for i in range(len(concat_data_list)):
        concat_data_list[i]+=f"{encryption_list[i]}"
    
    for i in range(len(concat_data_list)):
        data=concat_data_list[i]
        hash_dict[file_names[i]]=generate_hash(data.encode("utf-8"))
        signature_dict[file_names[i]]=create_signature(data,private_key_path,password)
    
    return file_metadata,encryption_dict,signature_dict,hash_dict

def main():
    
    while True:
        input_file_path=input("Enter The file to upload: ")
        server_list=_load_server_list(SERVER_LIST_PATH)
        print(server_list)
        no_server=len(server_list)

        print("..........Preparing files to send...................😉")
        file_metadata,encryption_dict,signature_dict,hash_dict=prepare_data_to_send(input_file_path,server_list,no_server,SERVER_PUBKEY_PATH)
        file_names=[name for name in file_metadata.keys()]
        metadata_list=[data for data in file_metadata.values()]
        encryption_list=[enc for enc in encryption_dict.values()]
        signature_list=[sign for sign in signature_dict.values()]
        hash_list=[hash for hash in hash_dict.values()]
        print("Files prepared.....😀") 

        print("..Sending files to the server..🛸")
        ack_list=[]
        for i,(server_host,server_port) in enumerate(server_list):
            data_to_send={
                "file_name":file_names[i],
                "file_metadata":metadata_list[i],
                "encrypted_file":encryption_list[i],
                "signed_hash":signature_list[i],
                "folder_id":i,
            }
            ack=send_data_to_server(server_host,server_port,data_to_send)
            ack_list.append(ack)
        print("..Data sent to all servers waiting for acknowledgement..🧐")

        
        flag=True
        for i in range(len(hash_list)):
            flag=flag and verify_signature(ack_list[i],hash_list[i],SERVER_PUBKEY_PATH)
        
        
        if flag:
            print("..Verification sucessfull..✅\n")
            print("..Data uploaded sucessfully..✨✨\n")
            print("..Deleting files from local..🗑️\n")
            shutil.rmtree("client_cache")
        else:
            print("..something wrong please try resending..")


if __name__=="__main__":
    main()


