import io
import pandas as pd
import json
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET,API_NAME,API_VERSION,SCOPES)

file_names = []
file_ids = []

page_token = None
while True:
    response = service.files().list(q="fullText contains 'Google Alerte : CO2.json'",spaces='drive',fields='nextPageToken, files(id, name)',pageToken=page_token).execute()
    for file in response.get('files', []):
        print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        file_names.append(file.get('name'))
        file_ids.append(file.get('id'))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break

for file_id, file_name in zip(file_ids, file_names):
        file = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, file)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        with open('alerts.json', 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
            f.close()

with open('alerts.json', 'r') as f:
    datastore = json.load(f)

url = []
for i in range(0, len(datastore)):
    for y in range(0, len(datastore[str(i)]["cards"][0]["widgets"])):
        url.append(datastore[str(i)]["cards"][0]["widgets"][y]["url"])

pd.DataFrame(url).to_csv('urlList.csv')
