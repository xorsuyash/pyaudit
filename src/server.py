from encryption.encrypt import decrypt_data
from client_utils import create_signature
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
    
    #preparing acknowledgement 
    concatenated_data=""
    for i in range(len(file_metadata)):
        concatenated_data+=f"{file_metadata[i]}"
    concatenated_data+=f"{encrypted_data}"

    ack=create_signature(concatenated_data,SERVER_PRIVATEKEY_PATH,"suyash123@")
    print("SENDING ACKNOWLEDGEMENT FOR VERIFICATION..⏳")
    client_socket.sendall(str(ack).encode())


    



    response="Data received sucessfully"
    client_socket.sendall(response.encode())



"""PORT=5050
HEADER=64 
FORMAT="utf-8"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
DISCONNECT="Disconnect"
UPLOAD_DIRECTORY="uploads"

os.makedirs(UPLOAD_DIRECTORY,exist_ok=True)

acl_dict={}

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected=True 
    try:
        while connected:
            msg_length=conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break 

            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            
            
            if msg==DISCONNECT:
                connected=False 
            elif msg.startswith("!upload "):
                upload_file(conn,msg.split(" ")[1])
            elif msg.startswith("!acl "):
                update_acl(msg.split(" ",2)[1],msg.split(" ",2)[2])
            elif msg.startswith("!download "):
                download_file(conn,msg.split(" ")[1])
            else:
                print(f"{addr}: {msg}")
    
    except Exception as e:
        print(f"[ERROR] exception in handle_client for {addr}: {e}")

    finally:
        conn.close()
        print(f"[CONNECTION CLOSED] {addr} disconnected")


def upload_file(conn,filename):
    try:
        file_size=int(conn.recv(HEADER).decode(FORMAT))
        file_path=os.path.join(UPLOAD_DIRECTORY,filename)

        with open(file_path,'wb') as file:
            data=conn.recv(file_size)
            file.write(data)

        print(f"File '{filename}' uploaded sucessfully")
    except Exception as e:
        print(f"[ERROR] Exception in upload_file: {e}")

def update_acl(filename,acl):
    try:
        acl_dict[filename]=acl 
        print(f"Acess controll list for '{filename}': {acl}")
    except Exception as e:
        print(f"[ERROR] Exception in update_acl: {e}")

def download_file(conn,filename):
    try:
        file_path= os.path.join(UPLOAD_DIRECTORY,filename)

        if os.path.exists(file_path):
            with open(file_path,'rb') as file:
                file_data=file.read()
            
            if filename in acl_dict:
                acl=acl_dict[filename]
                client_addr=conn.getpeername()[0]
                if client_addr not in acl:
                    print(f"Acess denied: {client_addr} does not have acess to {filename}")
                    return 
            
            conn.send(str(len(file_data)).encode(FORMAT))

            conn.send(file_data)
            print(f"File '{filename}' sent to {conn.getpeername()[0]}")
        
        else:
            print(f"FILE '{filename}' not found on the server")
        
    except Exception as e:
        print(f"[ERROR] Exceptiion in download_file: {e}")


def start():
    try:
        server.listen()
        print(f"[LISTENING] server is listening on {SERVER}")
        while True:
            conn,addr=server.accept()
            thread=threading.Thread(target=handle_client,args=(conn,addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        
    except Exception as e:
        print(f"[ERROR] Exception in start: {e}")
    
    finally:
        server.close()


print("[STARTING] server is starting")
start()"""