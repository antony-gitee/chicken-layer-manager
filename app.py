from flask import Flask, request, jsonify, abort
import config
from models import db, Chicken
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Create tables on startup
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return jsonify({"message": "Chicken Layer Manager API is running!"})

# --------- Chicken CRUD ---------
@app.route("/chickens", methods=["POST"])
def create_chicken():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    try:
        c = Chicken(name=name, breed=data.get("breed"), age=data.get("age"))
        db.session.add(c)
        db.session.commit()
        return jsonify(c.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/chickens", methods=["GET"])
def list_chickens():
    chickens = Chicken.query.order_by(Chicken.id).all()
    return jsonify([c.to_dict() for c in chickens]), 200

@app.route("/chickens/<int:chicken_id>", methods=["GET"])
def get_chicken(chicken_id):
    c = Chicken.query.get_or_404(chicken_id)
    return jsonify(c.to_dict()), 200

@app.route("/chickens/<int:chicken_id>", methods=["PUT"])
def update_chicken(chicken_id):
    c = Chicken.query.get_or_404(chicken_id)
    data = request.get_json() or {}
    c.name = data.get("name", c.name)
    c.breed = data.get("breed", c.breed)
    c.age = data.get("age", c.age)
    try:
        db.session.commit()
        return jsonify(c.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/chickens/<int:chicken_id>", methods=["DELETE"])
def delete_chicken(chicken_id):
    c = Chicken.query.get_or_404(chicken_id)
    try:
        db.session.delete(c)
        db.session.commit()
        return jsonify({"message": f"Chicken {chicken_id} deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
