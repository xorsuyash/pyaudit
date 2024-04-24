from encryption.encrypt import decrypt_data
from encryption.hash import generate_hash,generate_signature
from server_utils import build_tree
import socket 
import os 

SERVER_PRIVATEKEY_PATH="/home/suyash/pyaudit/src/server_configs/private_key.pem"

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
    save_path=os.path.join('uploads',save_folder_id,file_name)
    with open(save_path,'w') as f:
          f.write(decrypted_data.decode())
    
    #preparing acknoledgement 
    ack=generate_ack(file_metadata,encrypted_data,"suyash123@")
    
    print("SENDING ACKNOWLEDGEMENT FOR VERIFICATION..⏳")
    client_socket.sendall(ack)


def handle_regular_client():
     
    client_socket,client_address=server_socket.accept()

    directory_path=''
    tree=build_tree(directory_path,indent='')

    #listing all the files in the directory
    client_socket.sendall(tree.encode())

    #receiving file name 
    file_name=client_socket.recv(1024)

    with open(file_name,'r') as f:
        file_data=f.read()
    
    #preparing data to send 
    #file metadata 
    #file name 
    #encrypted file 
    #signed hash 
    #send file to client    





def main():
    
    while True:
         handle_data_owner()

if __name__=='__main__':
     main()
    