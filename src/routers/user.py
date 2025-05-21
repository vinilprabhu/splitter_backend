from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import create_access_token, get_current_user
from src.models.user import User
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
from passlib.context import CryptContext
from src.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register")
async def register(user: UserCreate):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = User(
        name=user.name,
        email=user.email,
        password_hash=pwd_context.hash(user.password),
        created_at=datetime.now(timezone.utc)
    )
    
    new_user = await User.insert_one(user_doc)
    
    return {"message": "User created successfully", "id": str(new_user.id)}

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user_doc = await User.find_one(User.email == form_data.username)
    
    if not user_doc or not pwd_context.verify(form_data.password, user_doc.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user_doc.id)}, expires_delta=None)
    return Token(access_token=token)

@router.post("/verify_login")
async def verify_login(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Token is valid"}