from datetime import datetime, timedelta
import jwt
from typing import Optional


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


def sign_jwt(email: str) -> str:
    # создание токена
    payload = {
        'email': email,
        'expires': (datetime.utcnow() + timedelta(days=14)).strftime('%d/%m/%Y %H:%M')
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str) -> Optional:
    # декодирование токена
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if datetime.strptime(decoded_token['expires'], '%d/%m/%Y %H:%M') >= datetime.utcnow():
            return decoded_token
        else:
            return None
    except Exception as e:
        return {'error': e}
