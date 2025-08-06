from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/retrieve_data.php")
def retrieve_data():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    fake_db = {
        "123": {
            "user_id": "123",
            "transaction_id": "tx987654321",
            "spoof_ip": "123.123.123.123"
        }
    }

    data = fake_db.get(user_id)
    return jsonify([data] if data else [])

@app.route("/update_liveness.php", methods=["POST"])
def update_liveness():
    data = request.get_json()
    required_keys = {"user_id", "liveness_id", "spoof_ip", "transaction_id"}
    if not data or not required_keys.issubset(data):
        return jsonify({"error": "Missing data"}), 400

    with open("logs.txt", "a") as f:
        f.write(str(data) + "\n")

    return jsonify({"success": True})
