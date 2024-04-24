from encryption.encrypt import decrypt_data,encrypt_data
from encryption.hash import generate_hash,generate_signature
from server_utils import build_tree
import socket 
import os 
import json 
import threading 

SERVER_PRIVATEKEY_PATH="/home/suyash/pyaudit/src/server_configs/private_key.pem"
CLIENT_PUBLICKEY_PATH="/home/suyash/pyaudit/src/regular_client_configs/public_key.pem"

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',0))

server_address=server_socket.getsockname()

HOST,PORT=server_address[0],server_address[1]

print(f"Server running on {HOST}:{PORT}")


server_socket.listen()
print("Server is listening...👂")

def _extract_data(data):
     
     return data["file_name"],data["file_metadata"],data["encrypted_file"],data["signed_hash"],data["folder_id"]

def generate_ack(file_metadata,encrypted_data,password):
    
    concatenated_data=""

    for i in range(len(file_metadata)):
         concatenated_data+=f"{file_metadata[i]}"
    concatenated_data+=f"{encrypted_data}"

    hash=generate_hash(concatenated_data.encode("utf-8"))
    ack=generate_signature(hash,SERVER_PRIVATEKEY_PATH,password)

    return ack 

def handle_data_owner():
     
    client_socket,client_address=server_socket.accept()
    print(f"Received connection from {client_address}")

    data_bytes=client_socket.recv(4096)
    data_str=data_bytes.decode()
    data=eval(data_str)

    file_name,file_metadata,encrypted_data,signed_hash,folder_id=_extract_data(data)

    #uploading data 
    decrypted_data=decrypt_data(encrypted_data,SERVER_PRIVATEKEY_PATH,"suyash123@")
    save_folder_id=f"CSP{folder_id}"
    
    if not os.path.exists(f"uploads/{save_folder_id}"):
          os.makedirs(f"uploads/{save_folder_id}")
    
    save_file_path=os.path.join('uploads',save_folder_id,file_name)
    
    with open(save_file_path,'w') as f:
          f.write(decrypted_data.decode())
    
    base_file_name=os.path.splitext(file_name)[0]
    save_metadata_file_name=f".{base_file_name}.json"
    save_metadata_path=os.path.join('uploads',save_folder_id,save_metadata_file_name)
    
    with open(save_metadata_path,'w') as f:
         json.dump(file_metadata,f)    
    
    #preparing acknowledgement 
    ack=generate_ack(file_metadata,encrypted_data,"suyash123@")
    
    print("SENDING ACKNOWLEDGEMENT FOR VERIFICATION..⏳")
    client_socket.sendall(ack)


def handle_regular_client():
     
    client_socket,client_address=server_socket.accept()

    directory_path='/home/suyash/pyaudit/src/uploads/CSP0'
    tree=build_tree(directory_path,indent='')

    #listing all the files in the directory
    client_socket.sendall(tree.encode())

    #receiving file name 
    file_name=client_socket.recv(1024)

    folder_path=os.path.join("uploads","CSP0",f"{file_name.decode()}")

    with open(folder_path,'r') as f:
        file_data=f.read()
    
    base_file_name=os.path.splitext(file_name.decode())[0]
    meta_data_file_name=f".{base_file_name}.json"
    meta_data_folder_path=os.path.join("uploads","CSP0",f"{meta_data_file_name}")
    
    with open(meta_data_folder_path,'r') as f:
         metadata=json.load(f)
    
    metadata=list(metadata)

    encrypted_data=encrypt_data(file_data.encode("utf-8"),CLIENT_PUBLICKEY_PATH)
    
    concat_data=""
    for i in range(len(metadata)):
         concat_data+=f"{metadata[i]}"
    concat_data+=f"{encrypted_data}"

    hash=generate_hash(concat_data.encode("utf-8"))
    signature=generate_signature(hash,SERVER_PRIVATEKEY_PATH,"suyash123@")

    data_dict={"file_metadata":metadata,"encrypted_file":encrypted_data,"signed_hash":signature}

    client_socket.sendall(str(data_dict).encode())

    msg=client_socket.recv(1024)

    if msg.decode()=='Audit sucessfull':
         client_socket.close()
     
    else:
         send_report(msg,server_host,server_port)

def send_report(msg,server_host,server_port):
     pass 



def main():
    
    while True:
         handle_regular_client()
         """client_socket,address=server_socket.accept()

         if address==('127.0.0.1',2345):
              
              data_owner_thread= threading.Thread(target=handle_data_owner)
              data_owner_thread.start()

         else:
              regular_client_thread=threading.Thread(target=handle_regular_client)
              regular_client_thread.start()"""
               

if __name__=='__main__':
     main()
    