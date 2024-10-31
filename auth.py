from functools import wraps
from flask import request, jsonify, g
import jwt
import time
import bcrypt
from db import create_user, get_user_by_email, get_user_by_id

JWT_SECRET = 'your-secret-key'  # Store this securely in environment variables
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours in seconds


def signup():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if get_user_by_email(data.get('email')):
        return jsonify({'error': 'Email already registered'}), 400
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(data.get('password').encode('utf-8'), salt)
    
    try:
        user_id = create_user(
            email=data.get('email'),
            password=hashed,
            name=data.get('name')
        )
        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = get_user_by_email(data.get('email'))
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    stored_password = user['password']
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')
        
    if bcrypt.checkpw(data.get('password').encode('utf-8'), stored_password):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': int(time.time()) + JWT_EXPIRATION
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'email': user['email'],
            'user_id': user['id']
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.current_user = get_user_by_id(payload['user_id'])
            if not g.current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated

def get_current_user():
    return getattr(g, 'current_user', None)