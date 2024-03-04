import socket 

SERVER_PORT=5050 
HEADER=64 
FORMAT="utf-8"
DISCONNECT="!Disconnect"
SERVER=socket.gethostbyname(socket.gethostname())


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER,SERVER_PORT))


def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    client.send(send_length)
    client.send(message)


class RegularClient:

    @staticmethod
    def download_file(filename):
        send(f"!download {filename}")

        file_size=int(client.recv(HEADER).decode(FORMAT))

        if file_size>0:
            file_data=client.recv(file_size)

            with open(filename,'wb') as file:
                file.write(file_data)
            
            print(f"File '{filename}' downlaoded sucessfully")
        else:
            print(f"File '{filename}' not found on the server")
    

    @staticmethod
    def request_acess(filename):
        send(f"!request_acess {filename}")

        response=client.recv(2048).decode(FORMAT)
        print(response)

