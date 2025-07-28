from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("Mongo_URL"))
db = client["Studentsdata"]
users = db["students"]

@app.route('/')
def home():
    return "Welcome from backend", 200

@app.route('/data', methods=['GET', 'POST'])
def first():
    if request.method == 'GET':
        return jsonify({"message": "GET request received. Nothing to see here!"}), 200

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()

    if "email" not in data:
        return jsonify({"error": "Missing 'email' in request"}), 400

    if "phone" not in data:
        return jsonify({"error": "Missing 'phone' in request"}), 400    

    if users.find_one({"email": data["email"]}) or users.find_one({"phone": data["phone"]}):
        return jsonify({"message": "Message Already Sent"}), 400

    users.insert_one(data)
    return jsonify({"message": "Data inserted successfully"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
