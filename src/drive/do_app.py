import os 
import io 
from fastapi import FastAPI 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from googleapiclient.http import MediaIoBaseDownload 
from cryptography.fernet import Fernet 
from google.oauth2 import service_account


#credentials using the service 
SCOPES=['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE="pyaudit_creds.json"

#Build google drive service 
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the google drive services 
drive_service=build('drive','v3',credentials=credentials)

def create_folder(folder_name,parent_folder_id=None):
    """__DOCS__"""

    folder_metadata={
        'name':folder_name,
        "mimeType":"applications/vnd.google-apps.folder",
        'parents':[parent_folder_id] if parent_folder_id else []
    }

    created_folder=drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()

    print(f'Created Folder ID: {created_folder["id"]}')

    return created_folder["id"]


def list_folder(parent_folder_id=None,delete=False):
    """__DOCS__"""

    results=drive_service.files().list(
        q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
        pageSize=1000,
        fields="nextPageToken , files(id,name, mimeType)"
    ).execute()

    items=results.get('files',[])
    if not items:
        print("No folder and files found in google drive")
    else:
        print("Folder ans files in Google drive")

        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']},Type: {item['mimeType']}")
            if delete:
                delete_files(item['id'])


def delete_files(file_or_folder_id):
    """Delete a file or folder in Google Drive by ID."""
    try:
        drive_service.files().delete(fileId=file_or_folder_id).execute()
        print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
    except Exception as e:
        print(f"Error deleting file/folder with ID: {file_or_folder_id}")
        print(f"Error details: {str(e)}")

"""def download_file(file_id, destination_path):
    Download a file from Google Drive by its ID.
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, from google.oauth2 import service_account
de='wb')
    
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")"""

if __name__=="__main__":

    #create_folder("MyNewFolder")
    list_folder()