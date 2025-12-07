# auth/jwt_handler.py
import time
import jwt
from typing import Dict

JWT_SECRET = "please_please_update_me_please"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return {}
    except jwt.InvalidTokenError:
        print("Invalid token")
        return {}
    except Exception as e:
        print(f"Error decoding JWT: {str(e)}")
        return {}
