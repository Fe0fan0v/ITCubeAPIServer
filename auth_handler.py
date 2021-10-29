from datetime import datetime, timedelta
import jwt
from typing import Optional
from os import getenv
import uuid

JWT_SECRET = getenv('API_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')


def sign_jwt(email: str) -> str:
    # создание токена
    payload = {
        'email': email,
        'expires': (datetime.utcnow() + timedelta(days=14)).strftime('%d/%m/%Y %H:%M')
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return str(token)


def decode_jwt(token: str) -> Optional:
    # декодирование токена
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    if datetime.strptime(decoded_token['expires'], '%d/%m/%Y %H:%M') >= datetime.utcnow():
        return decoded_token
    else:
        return None
