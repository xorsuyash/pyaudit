from hash import generate_hash,generate_signature,verify_signature
from utils import generate_keys_and_save

if __name__=="__main__":

    #password="suyash123@"

    #generate_keys_and_save("private_key.pem","public_key.pem",password)

    #signature of the file to be sent 
    with open("file1.txt","r") as f:
        file_data=f.read()
    with open("private_key.pem","r") as f:
        private_key=f.read()
    hash=generate_hash(file_data.encode("utf-8"))
    signature=generate_signature(hash,"private_key.pem",password="suyash123@")

    # signature sent it to the server 
    with open("output1.txt") as f:
        received_data=f.read()
    with open("public_key.pem") as f:
        public_key=f.read()
    
    print(verify_signature(signature,received_data.encode("utf-8"),"public_key.pem"))
    
    """ client_data->hash->signature-------->server_data,signature,public_key_client, 
        |                                     |
        |_____________________________________|
    """
    # same data signature generates and send it to client and then cleint compares the data and signature, if verified then send it then deletes the files on the server
    # prints data sucessfully uploaded 