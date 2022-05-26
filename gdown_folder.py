import io
import os
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

credential_json = {
    ### Create a service account and use its the json content here ###
    ### https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account
    ### credentials.json looks like this:
    "type": "service_account",
    "project_id": "############",
    "private_key_id": "###",
    "private_key": "-----BEGIN PRIVATE KEY-----###########3-----END PRIVATE KEY-----\n",
  "client_email": "#######",
  "client_id": "####",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "#############"
}

credentials = service_account.Credentials.from_service_account_info(credential_json)
drive_service = build('drive', 'v3', credentials=credentials)

folderId = "########Enter folder share id#########3"
outputFolder = 'output'

# Create folder if not existing
if not os.path.isdir(outputFolder):
    os.mkdir(outputFolder)

items = []
pageToken = ""
while pageToken is not None:
    response = drive_service.files().list(q="'" + folderId + "' in parents", pageSize=1000, pageToken=pageToken,
                                          fields="nextPageToken, files(id, name)").execute()
    items.extend(response.get('files', []))
    pageToken = response.get('nextPageToken')

for file in items:
    file_id = file['id']
    file_name = file['name']
    request = drive_service.files().get_media(fileId=file_id)
    ### Saves all files under outputFolder
    fh = io.FileIO(outputFolder + '/' + file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f'{file_name} downloaded completely.')
