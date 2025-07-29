from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
try:
    client = MongoClient(os.getenv("Mongo_URL"))
    db = client["Studentsdata"]
    users = db["students"]
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print("❌ Database connection failed:", e)

# Root route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "PIBITECH backend is running"}), 200

# Fetch raw student data (with _id)
@app.route('/test', methods=['GET'])
def test_fetch():
    try:
        all_students = list(users.find())
        return jsonify([str(s) for s in all_students]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch student list (excluding _id)
@app.route('/students', methods=['GET'])
def get_students():
    try:
        student_list = list(users.find({}, {"_id": 0}))
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new student
@app.route('/add-student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        users.insert_one(data)
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔒 Admin login route
@app.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
