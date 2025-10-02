from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Chicken Layer Manager API is running!"})

if __name__ == '__main__':
    app.run(debug=True)
