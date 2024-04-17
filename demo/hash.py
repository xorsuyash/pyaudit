from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import sys 


def generate_sginature(file_path):

    key=RSA.generate(2048)

    with open(file_path,'rb') as f:
        file_hash=SHA256.new(f.read())
    
    signer=pkcs1_15.new(key)
    signature=signer.sign(file_hash)

    with open('public_key.pem','wb') as f:
        f.write(key.publickey().export_key())
    
    with open('signature.bin','wb') as f:
        f.write(signature)
    

    print("Public key saved to 'public_key.pem")
    print("Signature saved to 'signature.bin'")


def main():
    if len(sys.argv)!=2:
        print("Usage: python generate_signature.py <file_path>")
    
    file_path=sys.argv[1]

    generate_sginature(file_path)

if __name__=='__main__':
    main()
