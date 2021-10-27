from fastapi import FastAPI, Header
from models import User, UserLogin, Profile, Message, Token, ErrorMessage
from fastapi.responses import JSONResponse
import database
from auth_handler import sign_jwt, decode_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Union, Optional
from fastapi.middleware.cors import CORSMiddleware
from os import environ
from verify_email import validate_user


app = FastAPI()
API_KEY = environ['API_KEY']  # ключ для шифрования находится в переменной окружения
origins = ["*"]   # настройка CORS. В данном случае разрешены любые запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def check_user(data: UserLogin) -> dict:
    # метод проверяет данные введенные пользователем при авторизации
    user = await database.find_user({'email': data.email})
    if not user:
        return {'error': 'Wrong email'}
    elif not check_password_hash(user['password'], data.password):
        return {'error': 'wrong password'}
    else:
        return user


async def check_token(token: str) -> Optional:
    # метод проверяет токен пользователя
    email = decode_jwt(token)['email']
    user = await database.find_user({'email': email})
    return user if user else False


@app.get("/")
async def index():
    # сообщение на главной
    return {"message": "Welcome to ITCube Server. To read documentation you should go to /docs path"}


@app.post('/register',
          tags=['Registration'],
          response_model=Token,
          responses={409: {'content': {
                              'application/json': {'example': {'error': 'User already exists'}}}}}
          )
async def create_user(user: UserLogin) -> Union[dict, JSONResponse]:
    # метод регистрации пользователя
    founded = await database.find_user({'email': user.email})
    if not founded:
        user.password = generate_password_hash(user.password)
        user = User(**user.dict())
        user = await database.add_user(user.dict())
        return {'token': sign_jwt(user['email'])}
    else:
        return JSONResponse(status_code=409,
                            content={'error': 'User already exists'})


@app.post('/auth',
          tags=['Authorization'],
          response_model=Token,
          responses={402: {
              'model': Message,
              'content': {
                              'application/json': {'example': {'error': 'Wrong password'}}}}}
          )
async def login_user(user: UserLogin) -> Union[dict, JSONResponse]:
    # метод авторизации пользователя
    response = await check_user(user)
    if 'email' in response.keys():
        return {'token': sign_jwt(response['email'])}
    return JSONResponse(status_code=402,
                        content=response)


@app.get('/profile',
         tags=['Profile'],
         response_model=Profile,
         responses={403: {'model': Message,
                          'content': {'application/json': {'example': {'error': 'Token is incorrect'}}}}}
         )
async def user_profile(*, token: str = Header(None, example={'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1hcnlAbWFpbC5ydSIsImV4cGlyZXMiOiIwMi8xMS8yMDIxIDA0OjIwIn0.s-kv8W9X1qEko3Qyom0akP81hgt4DHF2Ex4p__3GBj8'})) -> Union[Profile, JSONResponse]:
    # метод возвращает информацию по профилю пользователя, валидация по токену
    response = await check_token(token)
    if type(response) == dict:
        del response['password']
        del response['public_id']
        return Profile(**response)
    else:
        return JSONResponse(status_code=403,
                            content={'error': 'Token is incorrect'})


@app.get('/email-verify/')
async def verify_email(token: str) -> Union[Message, ErrorMessage]:
    return await validate_user(token)