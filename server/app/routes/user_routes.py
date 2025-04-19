from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.services import user_service
from app.core import auth

router = APIRouter()


@router.post("/signup")
async def signup(data: UserCreate):
    exists = await user_service.get_user_by_email(data.email)
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    await user_service.create_user(data.dict())
    return {"message": "User created"}


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    user = await user_service.get_user_by_email(data.email)
    if not user or not await user_service.verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = await auth.create_access_token(str(user.id), user.role)
    refresh_token = await auth.create_refresh_token(str(user.id))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: str):
    payload = await auth.verify_refresh_token(token)
    access_token = await auth.create_access_token(payload["sub"], role="USER")
    refresh_token = await auth.create_refresh_token(payload["sub"])
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
