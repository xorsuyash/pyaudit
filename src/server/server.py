import socket 
import threading 
import os 


HOST=''




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