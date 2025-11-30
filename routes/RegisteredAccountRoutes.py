# routes/RegisteredAccountRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.RegisteredAccountController import (
    create_registered_account, get_all_registered_accounts, get_registered_account_by_number
)
from pydantic import BaseModel

router = APIRouter(prefix="/registered-accounts", tags=["Registered Accounts"])

class RegisteredAccountCreate(BaseModel):
    account_number: str
    ifsc_code: str
    phone_no: str
    email: str
    bank_id: int
    account_balance: float = 0.0

class RegisteredAccountResponse(BaseModel):
    id: int
    account_number: str
    ifsc_code: str
    phone_no: str
    email: str
    bank_id: int
    account_balance: float

    class Config:
        from_attributes = True


@router.post("/", response_model=RegisteredAccountResponse, status_code=status.HTTP_201_CREATED)
def register_account(account: RegisteredAccountCreate, db: Session = Depends(get_db)):
    if get_registered_account_by_number(db, account.account_number):
        raise HTTPException(409, "Account already registered")

    new_acc = create_registered_account(
        db, account.account_number, account.ifsc_code,
        account.phone_no, account.email, account.bank_id, account.account_balance
    )
    db.commit()
    return new_acc

@router.get("/", response_model=list[RegisteredAccountResponse])
def list_registered_accounts(db: Session = Depends(get_db)):
    accounts = get_all_registered_accounts(db)
    return accounts