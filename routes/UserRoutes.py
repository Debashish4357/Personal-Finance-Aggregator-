# routes/UserRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.userController import (
    create_user, get_all_users, get_user_by_id, get_user_by_email,
    get_user_by_phone, update_user, delete_user
)
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
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

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[str] = None
    overall_balance_limit: Optional[float] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_no: str
    overall_balance_limit: Optional[float] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_admin(user: UserCreate, db: Session = Depends(get_db)):
    """Admin endpoint for creating users (use /signup for normal registration)"""
    try:
        # Normalize email for checking
        email_normalized = user.email.lower()
        
        if get_user_by_email(db, email_normalized):
            raise HTTPException(409, "Email already registered")
        if get_user_by_phone(db, user.phone_no):
            raise HTTPException(409, "Phone number already registered")

        new_user = create_user(db, user.name, email_normalized, user.password, user.phone_no)
        db.commit()
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Registration error: {str(e)}")
        raise HTTPException(500, "Internal server error during registration")


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get user error: {str(e)}")
        raise HTTPException(500, "Internal server error")


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = update_user(db, user_id, update_data.dict(exclude_unset=True))
        if not user:
            raise HTTPException(404, "User not found")
        db.commit()
        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Update user error: {str(e)}")
        raise HTTPException(500, "Internal server error")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        if not delete_user(db, user_id):
            raise HTTPException(404, "User not found")
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Delete user error: {str(e)}")
        raise HTTPException(500, "Internal server error")

@router.get("/", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

