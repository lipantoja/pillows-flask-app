import db
from flask import Flask, request

app = Flask(__name__)


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