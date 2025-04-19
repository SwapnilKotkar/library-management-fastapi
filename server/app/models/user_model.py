from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from enum import Enum


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models."""

    @classmethod
    def __get_validators__(cls):
        yield cls.__validate

    @classmethod
    def __validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserModel(BaseModel):
    """User model for the application."""

    id: Optional[PyObjectId] = Field(alias="_id")
    email: EmailStr
    hashed_password = str
    role: UserRole = UserRole.USER
    jti: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
