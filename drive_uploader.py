import os

SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = None  # ضع الـ ID الخاص بمجلد Drive هنا إن أردت

# تحقق مما إذا كان ملف الاعتماديات موجود
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    print("⚠️ WARNING: credentials.json not found. Google Drive upload disabled.")

    def upload_to_drive(file_path, filename):
        print(f"⛔ Skipped upload for {filename} (no credentials.json)")
        return None

else:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)

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
