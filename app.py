from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://pibitechcoursepage.vercel.app"}})


try:
    client = MongoClient(os.getenv("Mongo_URL"))
    db = client["Studentsdata"]
    users = db["students"]
    print(" Connected to MongoDB successfully")
except Exception as e:
    print(" Database connection failed:", e)

@app.route('/', methods=['GET'])
def home():
    return jsonify( "PIBITECH backend is running"), 200

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
        student_list = list(users.find({}, {"name": 1, "email": 1, "phone": 1, "_id": 0}))
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
