import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# إعداد الاعتماديات (credentials)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # هذا الملف حصلت عليه من Google Console

# إعداد Google Drive API
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# يمكن تخصيص مجلد معين لرفع الصور داخله (ضع ID المجلد إن أردت)
FOLDER_ID = None  # أو ضع ID هنا إذا كنت تريد مجلدًا معينًا

def upload_to_drive(file_path, filename):
    file_metadata = {'name': filename}
    
    if FOLDER_ID:
        file_metadata['parents'] = [FOLDER_ID]

    media = MediaFileUpload(file_path, mimetype='image/jpeg')

    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        print(f"✅ File uploaded: {filename} | ID: {file.get('id')}")
        print(f"🔗 Link: {file.get('webViewLink')}")
        return file.get('id')
    except Exception as e:
        print(f"❌ Error uploading {filename}: {str(e)}")
        return None
