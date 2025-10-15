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

@app.route("/chickens/<int:id>", methods=["GET"])
def get_chicken(id):
    chicken = Chicken.query.get(id)
    if not chicken:
        return jsonify({"error": "Chicken not found"}), 404
    return jsonify(chicken.to_dict()), 200

# ---- EggLog CRUD ----
@app.route("/egg_logs", methods=["POST"])
def create_egg_log():
    data = request.get_json()
    try:
        chicken_id = data.get("chicken_id")
        number_of_eggs = data.get("number_of_eggs")

        if not chicken_id or not number_of_eggs:
            return jsonify({"error": "chicken_id and number_of_eggs are required"}), 400

        # Check if chicken exists
        chicken = Chicken.query.get(chicken_id)
        if not chicken:
            return jsonify({"error": "Chicken not found"}), 404

        egg_log = EggLog(chicken_id=chicken_id, number_of_eggs=number_of_eggs)
        db.session.add(egg_log)
        db.session.commit()
        return jsonify(egg_log.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/egg_logs", methods=["GET"])
def list_egg_logs():
    logs = EggLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200


@app.route("/egg_logs/<int:log_id>", methods=["GET"])
def get_egg_log(log_id):
    log = EggLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Egg log not found"}), 404
    return jsonify(log.to_dict()), 200

# ---- FeedingLog CRUD ----
@app.route("/feeding_logs", methods=["POST"])
def create_feeding_log():
    data = request.get_json()
    try:
        chicken_id = data.get("chicken_id")
        feed_type = data.get("feed_type")
        quantity = data.get("quantity", 0)

        if not chicken_id or not feed_type:
            return jsonify({"error": "chicken_id and feed_type are required"}), 400

        # Check if chicken exists
        chicken = Chicken.query.get(chicken_id)
        if not chicken:
            return jsonify({"error": "Chicken not found"}), 404

        feeding_log = FeedingLog(chicken_id=chicken_id, feed_type=feed_type, quantity=quantity)
        db.session.add(feeding_log)
        db.session.commit()
        return jsonify(feeding_log.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/feeding_logs", methods=["GET"])
def list_feeding_logs():
    logs = FeedingLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200


@app.route("/feeding_logs/<int:log_id>", methods=["GET"])
def get_feeding_log(log_id):
    log = FeedingLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Feeding log not found"}), 404
    return jsonify(log.to_dict()), 200


@app.route("/feeding_logs/<int:log_id>", methods=["DELETE"])
def delete_feeding_log(log_id):
    log = FeedingLog.query.get(log_id)
    if not log:
        return jsonify({"error": "Feeding log not found"}), 404
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Feeding log deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
