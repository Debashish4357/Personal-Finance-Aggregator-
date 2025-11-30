# controller/RegisteredAccountController.py
from typing import Optional
from sqlalchemy.orm import Session
from schema.models import RegisteredUser


def create_registered_account(
    db: Session,
    account_number: str,
    ifsc_code: str,
    phone_no: str,
    email: str,
    bank_id: int,
    account_balance: float = 0.0
) -> RegisteredUser:
    reg = RegisteredUser(
        account_number=account_number,
        ifsc_code=ifsc_code,
        phone_no=phone_no,
        email=email,
        bank_id=bank_id,
        account_balance=account_balance
    )
    db.add(reg)
    db.flush()
    db.commit()
    db.refresh(reg)
    return reg


def get_registered_account_by_number(db: Session, account_number: str) -> Optional[RegisteredUser]:
    return db.query(RegisteredUser).filter(RegisteredUser.account_number == account_number).first()


def get_registered_account_by_bank(db: Session, bank_id: int) -> Optional[RegisteredUser]:
    return db.query(RegisteredUser).filter(RegisteredUser.bank_id == bank_id).first()

def get_all_registered_accounts(db: Session) -> list[RegisteredUser]:
    return db.query(RegisteredUser).all()  