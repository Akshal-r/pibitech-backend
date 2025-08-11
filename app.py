from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

CORS(app, origins=[
    "https://pibitech-course.vercel.app"], methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

try:
    mongo_url = os.getenv("Mongo_URL")
    client = MongoClient(mongo_url)
    db = client["Studentsdata"]
    users = db["students"]
    downloads = db["downloads"]
    courses = db["courses"]

    print(f"Connected to MongoDB: {mongo_url}")
    print(f"Collections: {db.list_collection_names()}")

except Exception as e:
    print("Database connection failed:", e)


@app.route('/', methods=['GET'])
def home():
    return jsonify("PIBITECH backend is running"), 200


@app.route('/students', methods=['GET'])
def get_students():
    try:
        student_list = list(users.find({}, {"_id": 0}))
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add-student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        if users.find_one({"email": data["email"]}):
            return jsonify({"message": "Email already registered"}), 400

        users.insert_one(data)
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/downloads', methods=['GET'])
def get_downloads():
    try:
        download_list = list(downloads.find({}, {"_id": 0}))
        return jsonify(download_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/log-download', methods=['POST'])
def log_download():
    try:
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Missing 'email' in request"}), 400

        data['downloaded_at'] = datetime.utcnow()
        downloads.insert_one(data)
        return jsonify({"message": "Download logged"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        course_list = list(courses.find({}, {"_id": 0}))
        return jsonify(course_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/courses', methods=['POST'])
def add_course():
    try:
        data = request.get_json()
        if not data or "title" not in data or "description" not in data or "modules" not in data:
            return jsonify({"error": "Missing required course fields"}), 400

        courses.insert_one(data)
        updated_courses = list(courses.find({}, {"_id": 0}))
        return jsonify(updated_courses), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
