import db
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import signup, login, require_auth, get_current_user

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

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

app.add_url_rule('/api/auth/signup', 'signup', signup, methods=['POST'])
app.add_url_rule('/api/auth/login', 'login', login, methods=['POST'])

@app.route('/api/protected')
@require_auth
def protected_route():
    current_user = get_current_user()
    return jsonify({
        'message': 'This is a protected route',
        'user': {
            'id': current_user['id'],
            'email': current_user['email'],
            'name': current_user['name']
        }
    })
