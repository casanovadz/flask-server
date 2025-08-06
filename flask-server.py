from flask import Flask, request, jsonify
import os
import json
from drive_uploader import upload_to_drive

app = Flask(__name__)
UPLOAD_FOLDER = 'selfies'
DB_FILE = 'db.json'  # ملف محلي لتخزين بيانات liveness_id
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Flask server is running.'

@app.route('/update_liveness', methods=['POST'])
def update_liveness():
    user_id = request.form.get('user_id', 'unknown_user')

    if 'selfie_file' in request.files:
        selfie_file = request.files['selfie_file']
        filename = f'{user_id}.jpg'
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        selfie_file.save(file_path)

        # حفظ البيانات إلى قاعدة بيانات محلية
        liveness_id = request.form.get('liveness_id', 'generated_' + user_id)
        save_liveness_id(user_id, liveness_id)

        # رفع الصورة إلى Google Drive
        upload_to_drive(file_path, filename)
    else:
        return jsonify({"status": "error", "message": "No selfie_file provided"})

    return jsonify({"status": "success", "message": "Selfie uploaded", "user_id": user_id})

@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify([])

    data = load_db()
    liveness_id = data.get(user_id)
    if not liveness_id:
        return jsonify([])

    return jsonify([{"user_id": user_id, "liveness_id": liveness_id}])

# مساعدة: تخزين واسترجاع من ملف JSON
def save_liveness_id(user_id, liveness_id):
    data = load_db()
    data[user_id] = liveness_id
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
