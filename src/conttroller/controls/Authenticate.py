from flask import request, jsonify, current_app
from functools import wraps
import jwt

from src.model.Usuario import Usuario

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({ "error": "You are not allowed to access this route" }), 403

        if not 'Bearer' in token:
            return jsonify({ "error": "Token is invalid"}), 401

        try:
            token_pure = token.replace('Bearer ', '')
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = Usuario.query.get(decoded['id'])


        except Exception as e:
            return jsonify({'error': str(e)})


        if current_user:
            return f(current_user=current_user, *args, **kwargs)
        else:
            return jsonify({ "error": "Token is invalid"}), 401

    return wrapper
