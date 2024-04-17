import sys
from data_owner_client import DataOwnerClient
from regular_client import RegularClient


def main():
    if len(sys.argv)<3:
        print("Usage: python3 client.py <CLIENT_TYPE> <COMMAND> [ARGS]")

        return 
    
    client_type=sys.argv[1].lower()
    command=sys.argv[2]


    if client_type == "dataowner" and command == "upload" and len(sys.argv)==4:
        
        DataOwnerClient.upload_file(sys.argv[3])

    elif client_type=="dataowner" and command=="acl" and len(sys.argv)==5:
        
        DataOwnerClient.update_acl(sys.argv[3],sys.argv[4])

    elif client_type=="regular" and command=="download" and len(sys.argv) ==4:

        RegularClient.download_file(sys.argv[3])

    elif client_type == "regular" and command == "request_access" and len(sys.argv) == 4:

        RegularClient.request_acess(sys.argv[3])
    else:
        print("Invalid command or arguments for specified client type")



if __name__=="__main__":
    
    main()