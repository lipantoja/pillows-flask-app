from functools import wraps
from flask import request, jsonify, g
import jwt
from datetime import datetime, timedelta
import bcrypt
from db import create_user, get_user_by_email, get_user_by_id

JWT_SECRET = 'your-secret-key'
JWT_EXPIRATION = 24 * 60 * 60

def signup():
    data = request.get_json()
    
    # Check for required fields
    required_fields = ['email', 'password', 'password_confirmation', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'errors': ['Missing required fields']}), 400
    
    # Validate password confirmation
    if data['password'] != data['password_confirmation']:
        return jsonify({'errors': ['Password confirmation does not match']}), 400
    
    # Check if user already exists
    if get_user_by_email(data['email']):
        return jsonify({'errors': ['Email has already been taken']}), 400

    # Hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    
    try:
        user_id = create_user(
            email=data['email'],
            password=hashed_password,
            name=data['name']
        )
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'errors': [str(e)]}), 400

def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'errors': ['Invalid email/password combination']}), 401

    user = get_user_by_email(data['email'])
    if not user:
        return jsonify({'errors': ['Invalid email/password combination']}), 401

    stored_password = user['password']
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')

    if bcrypt.checkpw(data['password'].encode('utf-8'), stored_password):
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        token = jwt.encode({
            'user_id': user['id'],
            'exp': int(expiration_time.timestamp())
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'jwt': token,
            'email': user['email'],
            'user_id': user['id']
        }), 201
    
    return jsonify({'errors': ['Invalid email/password combination']}), 401

def current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
        
    # Extract token from "Bearer <token>"
    token_match = auth_header.split(' ')
    if len(token_match) != 2:
        return None
        
    token = token_match[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = get_user_by_id(payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def authenticate_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({}), 401
        g.current_user = user
        return f(*args, **kwargs)
    return decorated