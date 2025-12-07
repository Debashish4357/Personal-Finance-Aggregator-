# routes/LoginRoutes.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.database import get_db
from schema.models import User
from auth.jwt_handler import signJWT
from pydantic import BaseModel, EmailStr, validator
from controller.userController import create_user, get_user_by_email, get_user_by_phone
import hashlib
import re

router = APIRouter(tags=["Auth"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, v):
        return v.lower()  # Convert to lowercase

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_no: str

    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip().title()  # Proper case formatting

    @validator('email')
    def validate_email(cls, v):
        return v.lower()  # Convert to lowercase

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

    @validator('phone_no')
    def validate_phone(cls, v):
        # Remove any non-digit characters including + and spaces
        phone_clean = re.sub(r'\D', '', v)
        if len(phone_clean) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        # For Indian numbers, remove country code if present
        if len(phone_clean) == 12 and phone_clean.startswith('91'):
            phone_clean = phone_clean[2:]
        elif len(phone_clean) == 13 and phone_clean.startswith('091'):
            phone_clean = phone_clean[3:]
        return phone_clean

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

@router.post("/signup")
def user_signup(user: UserSignup = Body(...), db: Session = Depends(get_db)):
    try:
        # Normalize email for checking
        email_normalized = user.email.lower()
        
        # Check if email already exists
        if get_user_by_email(db, email_normalized):
            raise HTTPException(status_code=409, detail="Email already registered")
        
        # Check if phone already exists
        if get_user_by_phone(db, user.phone_no):
            raise HTTPException(status_code=409, detail="Phone number already registered")

        # Create new user with normalized email
        new_user = create_user(db, user.name, email_normalized, user.password, user.phone_no)
        db.commit()
        
        # Return JWT token
        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "phone_no": new_user.phone_no
            },
            "token": signJWT(email_normalized)["access_token"]
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error during signup: {str(e)}")

@router.post("/login")
def user_login(user: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        # Normalize email for lookup
        email_normalized = user.email.lower()
        db_user = db.query(User).filter(User.email == email_normalized).first()
        if db_user and verify_password(user.password, db_user.password):
            return {
                "message": "Login successful",
                "user": {
                    "id": db_user.id,
                    "name": db_user.name,
                    "email": db_user.email,
                    "phone_no": db_user.phone_no
                },
                "token": signJWT(user.email)["access_token"]
            }
        raise HTTPException(status_code=401, detail="Invalid email or password")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during login")
