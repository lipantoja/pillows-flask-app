import db
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from auth import signup, login, authenticate_user

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173", "http://localhost:5000"],
    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/pillows.json")
def index():
    return db.pillows_all()

@app.route("/pillows.json", methods=["POST"])
def create():
    name = request.form.get("name")
    image_url = request.form.get("image_url")
    description = request.form.get("description")
    size = request.form.get("size")
    return db.pillows_create(name, image_url, description, size)

@app.route("/pillows/<id>.json")
def show(id):
    return db.pillows_find_by_id(id)

@app.route("/pillows/<id>.json", methods=["PATCH"])
def update(id):
    name = request.form.get("name")
    image_url = request.form.get("image_url")
    description = request.form.get("description")
    size = request.form.get("size")
    return db.pillows_update_by_id(id, name, image_url, description, size)

@app.route("/pillows/<id>.json", methods=["DELETE"])
def destroy(id):
    return db.pillows_destroy_by_id(id)

@app.route('/auth/signup', methods=['POST'])
def signup_route():
    return signup()

@app.route('/auth/login', methods=['POST'])
def login_route():
    return login()

@app.route('/auth/me', methods=['GET'])
@authenticate_user
def me():
    return jsonify({
        'user': {
            'id': g.current_user['id'],
            'email': g.current_user['email'],
            'name': g.current_user['name']
        }
    })

@app.after_request
def after_request(response):
    print(f"Response status: {response.status_code}")  # Debug print
    return response

if __name__ == "__main__":
    app.run(debug=True)
