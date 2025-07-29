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

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "PIBITECH backend is running successfully "}), 200

@app.route('/test', methods=['GET'])
def test_fetch():
    try:
        all_students = list(users.find())
        return jsonify([str(s) for s in all_students]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students', methods=['GET'])
def get_students():
    try:
        student_list = list(users.find({}, {"_id": 0}))
        print("Fetched Students:", student_list)  
        return jsonify(student_list), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=True)
