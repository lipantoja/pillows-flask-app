from flask import request, jsonify
import jwt
import time
import bcrypt
from db import create_user, get_user_by_email, get_user_by_id

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
    
    if user and bcrypt.checkpw(data.get('password').encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': int(time.time()) + JWT_EXPIRATION
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'jwt': token,
            'email': user['email'],
            'user_id': user['id']
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401