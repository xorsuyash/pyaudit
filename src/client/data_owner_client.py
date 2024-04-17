import socket 
import os 























"""SERVER_PORT=5050 
HEADER= 64 
FORMAT="utf-8"
DISCONNECT="!Disconnect"
SERVER=socket.gethostbyname(socket.gethostname())



client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER,SERVER_PORT))


def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

class DataOwnerClient:
    @staticmethod
    def upload_file(filepath):
        filename=os.path.basename(filepath)
        
        send(f"!upload {filename}")

        file_size=os.path.getsize(filepath)
        send(str(file_size))

        with open(filepath,'rb') as file:
            file_data=file.read()
            client.send(file_data)


    @staticmethod
    def update_acl(filename,acl):
        
        send(f"!acl {filename} {acl}")
        print(f"Acess control list for '{filename}' updated: {acl}")"""

