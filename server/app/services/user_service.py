from app.core.database import db
from app.models.user_model import UserModel, UserRole
from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_collection = db["users"]


async def create_user(data: dict):
    hashed = pwd_context.hash(data["password"])
    user = {"email": data["email"], "hashed_password": hashed, "role": UserRole.USER}
    await users_collection.insert_one(user)
    return True


async def get_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    return UserModel(**user) if user else None


async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return UserModel(**user) if user else None


async def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
