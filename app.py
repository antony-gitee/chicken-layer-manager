from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from config import Config
from extensions import db
from models import Chicken, EggLog, FeedingLog

app = Flask(__name__)
CORS(app)

# Load config and initialize db
app.config.from_object(Config)
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Chicken Layer Manager API is running!"})

# ---- Chicken CRUD ----
@app.route("/chickens", methods=["POST"])
def create_chicken():
    data = request.get_json()
    try:
        c = Chicken(name=data["name"], breed=data.get("breed"), age=data.get("age"))
        db.session.add(c)
        db.session.commit()
        return jsonify(c.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/chickens", methods=["GET"])
def list_chickens():
    chickens = Chicken.query.all()
    return jsonify([c.to_dict() for c in chickens]), 200

if __name__ == "__main__":
    app.run(debug=True)
