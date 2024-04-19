from encryption.encrypt import decrypt_data
from encryption.hash import generate_hash,generate_signature
import socket 
import threading 
import os 

SERVER_PRIVATEKEY_PATH="/home/suyash/pyaudit/src/server_configs/private_key.pem"

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',0))

server_address=server_socket.getsockname()

HOST,PORT=server_address[0],server_address[1]

print(f"Server running on {HOST}:{PORT}")

server_socket.listen()
print("Server is listening...👂")

while True:
    client_socket,client_address=server_socket.accept()
    print(f"Received connection from {client_address}")

    data_bytes = client_socket.recv(4096)
    data_str = data_bytes.decode()
    
    data=eval(data_str)

    #extracting information from received data
    file_name=data["file_name"]
    file_metadata=data["file_metadata"]
    encrypted_data=data["encrypted_file"]
    signed_hash=data["signed_hash"]
    folder_id=data["folder_id"]

    #Decrypting the data 
    decrypted_data=decrypt_data(encrypted_data,SERVER_PRIVATEKEY_PATH,"suyash123@")
    save_folder_id=f"CSP{folder_id}"
    if not os.path.exists(f"uploads/{save_folder_id}"):
        os.makedirs(f"uploads/{save_folder_id}")
    save_path=os.path.join('uploads',save_folder_id,file_name)
    with open(save_path,'w') as f:
        f.write(decrypted_data.decode())
    
    #preparing acknowledgement later will be inserted in the function  
    concatenated_data=""
    for i in range(len(file_metadata)):
        concatenated_data+=f"{file_metadata[i]}"
    concatenated_data+=f"{encrypted_data}"
    hash_ack=generate_hash(concatenated_data.encode("utf-8"))
    ack=generate_signature(hash_ack,SERVER_PRIVATEKEY_PATH,"suyash123@")

    print("SENDING ACKNOWLEDGEMENT FOR VERIFICATION..⏳")
    client_socket.sendall(ack)
    