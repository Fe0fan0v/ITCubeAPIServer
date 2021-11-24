import asyncio

from database import update_user, find_user
from models import Message, ErrorMessage
from typing import Union
from os import getenv
from itsdangerous import URLSafeSerializer
import smtplib


API_KEY = getenv('API_KEY')
HOST = 'smtp.yandex.ru'
FROM = getenv('EMAIL')
EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')


def create_verification_link(email: str) -> str:
    # метод возвращает ссылку для верификации email
    serializer = URLSafeSerializer(API_KEY)
    return f"http://itcubeserver.online/email-verify/?token={serializer.dumps(email, salt=API_KEY)}"


async def validate_user(token: str) -> Union[Message, ErrorMessage]:
    # метод валидирует email пользователя
    serializer = URLSafeSerializer(API_KEY)
    try:
        email = serializer.loads(token, salt=API_KEY)
        user = await find_user({'email': email})
        if not user:
            return ErrorMessage(**{'error': 'User doesn\'t exist'})
        elif user['validated']:
            return ErrorMessage(**{'error': 'User already validated'})
        elif await update_user(email, {'validated': True}):
            return Message(**{'message': 'Email validated successfully '})
        else:
            return ErrorMessage(**{'error': 'Validation failed'})
    except Exception as e:
        return ErrorMessage(**{'error': str(e)})


def send_email(email: str, to_send: dict) -> dict:
    ok = False
    try:
        body = '\n'.join((
            f'From: {FROM}',
            f'To: {email}',
            f'Subject: {to_send["subject"]}',
            '',
            to_send["text"]
        ))
        server = smtplib.SMTP_SSL(HOST)
        server.ehlo(FROM)
        server.login(FROM, EMAIL_PASSWORD)
        server.auth_plain()
        server.sendmail(FROM, email, body)
        server.quit()
        ok = True
    except Exception as e:
        return {'error': e}
    if ok:
        return {'OK': 'message sent'}

