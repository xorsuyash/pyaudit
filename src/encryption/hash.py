from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

def generate_hash(data):
    hash_obj=hashes.Hash(hashes.SHA256(),backend=default_backend())
    hash_obj.update(data)
    return hash_obj.finalize()

def generate_signature(hash_value,private_key_path,password):
        
    with open(private_key_path, "rb") as key_file:
            private_key_bytes = key_file.read()

    private_key = load_pem_private_key(
    private_key_bytes,
    password=password.encode() if password else None,
    backend=default_backend()
        )

    signature = private_key.sign(
        hash_value,
        padding.PKCS1v15(),
        hashes.SHA256()
        )
    return signature



def verify_signature(signature,data,public_key_path):


    with open(public_key_path,"rb") as key_file:
         public_key_bytes=key_file.read()
    
    public_key=load_pem_public_key(
         public_key_bytes,
         backend=default_backend()
    )


    try:
        public_key.verify(signature,
                          data,
                          padding.PKCS1v15(),
                          hashes.SHA256()
                          )
        return True 
    except InvalidSignature:
        return False 

