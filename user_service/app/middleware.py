import jwt
from functools import wraps
from flask import request, jsonify , g

SECRET_KEY = "AFPOJGPMPOMWEMPSDFONN&*321OINDSO"
ALGORITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "token is required"}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
            g.curret_user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"messasge": "Token is expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401
        
        return f(*args, **kwargs)
    return decorated