# routes/TransactionRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.TransactionController import (
    create_transaction, get_transaction_by_id, get_transactions_by_account
)
from schema.models import TransactionType, TransactionCategory
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/transactions", tags=["Transactions"])

class TransactionCreate(BaseModel):
    from_account_id: int
    transaction_type: TransactionType
    to_account_id: Optional[int] = None
    amount: float
    category: TransactionCategory
    balance_after_transaction: float
    transaction_date: Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: int
    from_account_id: int
    transaction_type: TransactionType
    amount: float
    category: TransactionCategory
    balance_after_transaction: float
    transaction_date: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def add_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    new_tx = create_transaction(
        db=db,
        from_account_id=tx.from_account_id,
        transaction_type=tx.transaction_type,
        to_account_id=tx.to_account_id,
        amount=tx.amount,
        category=tx.category,
        balance_after_transaction=tx.balance_after_transaction,
        transaction_date=tx.transaction_date
    )
    db.commit()
    return new_tx


@router.get("/account/{account_id}")
def get_account_transactions(
    account_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    transactions = get_transactions_by_account(db, account_id, limit, skip)
    return transactions