from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User, db

import validators


auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error':'Password is too short'}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error':'username too short'}), HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return jsonify({'error':'username should be alphanumeric char and no spaces'}), HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({'error':"Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
         return jsonify({'error':"Email already exists"}), HTTP_409_CONFLICT
    if User.query.filter_by(username=username).first() is not None:
         return jsonify({'error':"Username already exists"}), HTTP_409_CONFLICT
    pwd_hash = generate_password_hash(password)

    user = User(
        username=username,
        password = pwd_hash,
        email=email
        )
    db.session.add(user)
    db.session.commit()

    return  jsonify({
        'message':"User created",
        'user':{
            'username': username,
            "email": email,

        } 
    }), HTTP_201_CREATED
    
    return "User Created"

@auth.get('/user')
def currentUser():
    return {"user": "me"}

