# controller/UserController.py
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from schema.models import User
from datetime import datetime
import hashlib


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    phone_no: str
) -> User:
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    user = User(name=name, email=email, password=hashed_pw, phone_no=phone_no)
    db.add(user)
    db.flush()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone_no: str) -> Optional[User]:
    return db.query(User).filter(User.phone_no == phone_no).first()


def update_user(db: Session, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    db.flush()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        return True
    return False

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()