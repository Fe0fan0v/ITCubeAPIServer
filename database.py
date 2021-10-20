import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DB = 'mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
database = client.itcube
users = database.get_collection('users')


def user_helper(user) -> dict:
    return {
        'id': str(user['_id']),
        'public_id': user['public_id'],
        'name': user['name'],
        'surname': user['surname'],
        'email': user['email'],
        'password': user['password'],
        'role': user['role'],
        'courses': user['courses'],
        'validated': user['validated'],
        'birthday': user['birthday'],
        'registration_date': user['registration_date']
    }


async def find_users():
    founded = []
    async for user in users.find():
        founded.append(user_helper(user))
    return founded


async def add_user(user_data: dict) -> dict:
    user = await users.insert_one(user_data)
    new_user = await users.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def find_user(params: dict) -> dict:
    user = await users.find_one(params)
    if user:
        return user_helper(user)


async def update_user(email: str, data: dict):
    if len(data) < 1:
        return False
    user = await users.find_one({"email": email})
    if user:
        updated_user = await users.update_one(
            {"email": email}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(email: str):
    user = await users.find_one({"email": email})
    if user:
        await users.delete_one({"email": email})
        return True
