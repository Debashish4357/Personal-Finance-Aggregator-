# routes/LoginRoutes.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.database import get_db
from schema.models import User
from auth.jwt_handler import signJWT
from pydantic import BaseModel, EmailStr
import hashlib

router = APIRouter(tags=["Login"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

@router.post("/login")
def user_login(user: UserLogin = Body(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and verify_password(user.password, db_user.password):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail="Invalid login details!")
