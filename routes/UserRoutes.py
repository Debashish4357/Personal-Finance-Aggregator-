# routes/UserRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.userController import (
    create_user, get_all_users, get_user_by_id, get_user_by_email,
    update_user, delete_user
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone_no: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_no: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_no: str

    class Config:
        from_attributes = True


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(409, "Email already registered")
    if get_user_by_email(db, user.phone_no):  # assuming phone_no unique
        raise HTTPException(409, "Phone number already registered")

    new_user = create_user(db, user.name, user.email, user.password, user.phone_no)
    db.commit()
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, update_data.dict(exclude_unset=True))
    if not user:
        raise HTTPException(404, "User not found")
    db.commit()
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(404, "User not found")
    db.commit()
    return None

@router.get("/", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

