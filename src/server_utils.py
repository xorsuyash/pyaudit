import os 
import sys 
from encryption.utils import generate_keys_and_save
 

def generate_keys():

    if not os.path.exists('server_configs'):
        os.makedirs('server_configs')
    
    private_key_file_path=os.path.join('server_configs','private_key.pem')
    public_key_file_path=os.path.join('server_configs','public_key.pem')

    password="suyash123@"

    generate_keys_and_save(private_key_file_path,public_key_file_path,password)

    return private_key_file_path,public_key_file_path,password


def build_tree(directory_path,indent=''):
     
    tree=""

    if not os.path.isdir(directory_path):
          tree+=f"{indent}- {directory_path}\n"
          return tree 

    tree+=f"{indent}+ {os.path.basename(directory_path)}\n" 

    for item in os.listdir(directory_path):
         item_path=os.path.join(directory_path,item)
         if os.path.isdir(item_path):
              tree+=build_tree(item_path,indent + '  ')
         else:
              tree+=f"{indent} - {item}\n"
    
    return tree 

if __name__=='__main__':
    
    print(build_tree('/home/suyash/pyaudit/src/uploads/CSP0'))