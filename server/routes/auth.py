
from fastapi import APIRouter, HTTPException
from models import UserRegister, UserLogin
from database import users_collection
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserRegister):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {
        "name":     user.name,
        "email":    user.email,
        "password": hash_password(user.password),
        "role":     "user"
    }
    await users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}
