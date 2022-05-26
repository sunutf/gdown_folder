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
    "project_id": "fcvid-351408",
    "private_key_id": "f769e2333405328a2c55495ae36c90d5bb2a83ff",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZYxGIrh/GDRTy\nDh3JacOaGn0Fo8PmC1OrT2OALFe2Ph16bW1g9t0Yv5KWQpW0nSW940n6FqNwi2kD\nYqThxV8GVG5+CuV6jDz4Oo0ZwpF06pnPuQomop/xnqfj2quCYeORrxK4ibjxvFCZ\nNJyEWXeoPh0oJftgRpkmgFr1bh91B+8F0roj7ZVOpUuOWSsvV40beiyvyDU+LmAW\nCcEgA5nToY5eCrxD1QaYAkcDCBjj45XtLzdgIyF3sctmj5b5BVWecQhi9DWsHjoF\nE6r1tLnAAG0WrYWAklKVZF0f/OeffwGdt4EJK3DVxXm+hj5y2jps7zAa5133fFl/\nPHuBVXgvAgMBAAECggEAKcb77ZhPeyfw/oStxEAUUJLKXpDeOHf5T/2NgkmRkkeU\ny9WmJvTV/3meOWLlV449y1xut7kWxv6RmaRyeDPDz/uLJLVfD2PG720zJUMDTy7e\nud8STreYjLzDyaGzeQ2kZ/ehR7XrM5ww76mOv9WGa8KPOnIt52kTKZNoMtTNqJgW\njOjYzYlWW/eR3mTSlzWviTCuM6xllWgzsiaiY5VLcIsAEHBuAvb15KepBJkADccu\nfGbvBr0qnGmhtYeyw1q6ZNcMH4RbO8+cK4aOQdcmUH9rjvKHOB221swMzZ+ML4Ti\n1fWBxMH/H7VsiEoBA9L0CES1vRRFy6ygNPNWS2ht0QKBgQDO0zTzjfMVUQGMC5tD\nrnq57VkciqhqOSZSGm/uCRH9FGj6FqbeLtGsUbyrlQt2C5N5Jke0OsewsQLhHzE7\n/nMNPBeJqV1WsItpxUhFLwUlB7ulos3LJoucvl1IHW7g+OoZgIBizWV69WqcT0iT\nwYLjbbY2sB+LEnj8qKzhHSxcRQKBgQC920FN6LMbuSxXVTYS7f/O3XfW2+pWc+zC\nxQpI47g7Dan8Jlb0F0s4mwm4gs+QpgNaBawPRPavT+bJ75Oz0zmY2Pa5WIvYhsp9\nBavgpoLyfbrA4PwQl/gYww0cgET4z1qslXOWNnEHx3MoC1t6l9A2y+0FNYPjiCFH\n/ccdzuj74wKBgQCfrtPYI0WFtLhUDvX+aGzathSyA6AJ+zvJ8h1vE9OuqR5v0CNf\nsZgyyhy4AOgLaN6gj9yWmzdoBRKrCzExF8BufHHT2E53SvEoZafpumbnczP+q1bm\nPUlXaGaO8iKUUbo0nFEDd3+dUnPQYSow4hwTSbaAPLTt5AJDWFu5ppOEXQKBgB8k\nXdvntalwgGN66LnGLFXEYinuPMwdi9KO+5blM40MOrvPlifHwmDwnXGUk3OIp7gW\nghinGUe8dYDeOX4fwazeuenBKn9D7OcBDSZ2abhZA08sGGyoYNu+8uGf8LBXYuo4\nQZN8LqI2Bx+kbUb4rACxBpn6Iz4pUDw81nJ/RBw9AoGAQW0KCgWiwizAw3hHM6wP\nnbc2SC4eBdqBVPubBh4LiMQnPNN5b9zTB2xL/B3B2R2XHL7GIiSXvRGeDQVvQh7/\nKgt5s//YkHv6hTmQBjHWB+gNjMWQM8TJqmelNwlU5KLqVHde2A/K/mxnuki2StEE\nM40w1IxGWSG4kHm/LxxJkwk=\n-----END PRIVATE KEY-----\n",
  "client_email": "fcvid-364@fcvid-351408.iam.gserviceaccount.com",
  "client_id": "111877664303367363251",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fcvid-364%40fcvid-351408.iam.gserviceaccount.com"
}

credentials = service_account.Credentials.from_service_account_info(credential_json)
drive_service = build('drive', 'v3', credentials=credentials)

folderId = "1oBp2TgkoMA02Wa-BgqcdAUoLbIZUFDVi"
#folderId = '1cPSc3neTQwvtSPiVcjVZrj0RvXrKY5xj'
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
