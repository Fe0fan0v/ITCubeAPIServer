# модуль содержит модели
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict
import uuid


class User(BaseModel):
    # модель экземпляра пользователя
    public_id: str = Field(default=uuid.uuid4(), unique=True)
    name: Optional[str] = Field()
    surname: Optional[str] = Field()
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(default='entrant')
    validated: bool = Field(default=False)
    birthday: Optional[datetime] = Field()
    registration_date: datetime = Field(default=datetime.now())
    avatar: Optional[str] = Field()
    groups: Optional[list] = Field(default=[])

    class Config:
        schema_extra = {
            "example": {
                "name": "Иван",
                "surname": "Иванов",
                "email": "ivanov@mail.ru",
                "password": "hashed_password",
                "role": "student",
                "validated": "true",
                "birthday": "25.12.2002",
                "registration_date": "25.12.2020",
                "avatar": "storage.yandex.org/picture.jpg",
                "groups": [{
                    "group_name": 'Разработка VR/AR приложений(Базовый уровень)',
                    "schedule": "ПН: 9:00, ПТ: 9:00",
                    "students": ['Иванов', 'Петров', 'Сидоров']
                }]
            }
        }


class Course(BaseModel):
    # модель эксземпляра курса
    id: str
    course_name: str = Field(...)
    ages: str = Field(...)
    direction: str = Field(...)
    duration: str = Field(...)
    teachers: list = Field(default=[])

    class Config:
        schema_extra = {
            "example": {
                "course_name": 'Разработка VR/AR приложений',
                "ages": "12+",
                "direction": "VR/AR",
                "duration": "1",
                "teachers": ['Емельяненко М.А.', 'Уткин В.Л.']
            }
        }


class Group(BaseModel):
    # модель экземпляра группы
    group_name: str = Field(...)
    schedule: str = Field(...)
    students: list = Field(default=[])

    class Config:
        schema_extra = {
            "example": {
                "group_name": 'Разработка VR/AR приложений(Базовый уровень)',
                "schedule": "ПН: 9:00, ПТ: 9:00",
                "students": ['Иванов', 'Петров', 'Сидоров']
            }
        }


class UserLogin(BaseModel):
    # модель запроса авторизации (при регистрации используется она же)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": 'user@gmail.com',
                "password": 'password123'
            }
        }


class Profile(BaseModel):
    # модель профиля пользователя
    id: str
    name: str = None
    surname: str = None
    email: EmailStr
    role: str
    validated: bool
    birthday: datetime = None
    registration_date: datetime
    groups: Optional[list] = Field(default=[])
    avatar: Optional[str] = Field()

    class Config:
        schema_extra = {
            "example": {
                "id": '616e424fff0d52bb0e29ce45',
                "name": "Jhon",
                "surname": "Doe",
                "email": "jhon@gmail.com",
                "role": "entrant",
                "validated": False,
                "birthday": "2004-10-19",
                "registration_date": "2021-10-19T08:58:03.277000",
                "groups": [{
                    "group_name": 'Разработка VR/AR приложений(Базовый уровень)',
                    "schedule": "ПН: 9:00, ПТ: 9:00",
                    "students": ['Иванов', 'Петров', 'Сидоров']
                }],
                "avatar": "https://storage.yandexcloud.net/itcubeimages/avatar.jpg"
            }
        }


class Message(BaseModel):
    # модель сообщения
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": 'User validated successfully',
            }
        }


class ErrorMessage(BaseModel):
    # модель сообщения об ошибке
    error: str

    class Config:
        schema_extra = {
            "example": {
                "error": 'error message',
            }
        }


class Token(BaseModel):
    # модель токена
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1hcnlAbWFpbC5ydSIsImV4cGlyZXMiOiIwMi8xMS8yMDIxIDA0OjIwIn0.s-kv8W9X1qEko3Qyom0akP81hgt4DHF2Ex4p__3GBj8',
            }
        }


class Courses(BaseModel):
    # модель списка курсов
    courses: List[Course]

    class Config:
        schema_extra = {
            "example": {
                "courses": [
                    {
                        "id": "61ab55e7f998d9868472a122",
                        "course_name": "Разработка VR/AR приложений",
                        "ages": "12+",
                        "direction": "VR/AR",
                        "duration": "1+",
                        "teachers": []
                    },
                    {
                        "id": "61ab8b47ec690045c1f8ceb1",
                        "course_name": "3D-моделирование",
                        "ages": "12+",
                        "direction": "VR/AR",
                        "duration": "1+",
                        "teachers": []
                    },
                    {
                        "id": "61ab8b47ec690045c1f8ceb2",
                        "course_name": "Кибергигиена(BigData)",
                        "ages": "10+",
                        "direction": "Цифровая гигиена и Big Data",
                        "duration": "1",
                        "teachers": []
                    }
                ]
            }
        }


class EditProfile(BaseModel):
    Dict

    class Config:
        schema_extra = {
            "example": {
                "name": "Иван",
                "surname": "Иванов",
            }
        }