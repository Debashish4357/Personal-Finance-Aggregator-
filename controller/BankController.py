# controller/BankController.py
from typing import List, Optional
from sqlalchemy.orm import Session
from schema.models import Bank


def create_bank(db: Session, bank_name: str) -> Bank:
    bank = Bank(bank_name=bank_name)
    db.add(bank)
    db.flush()
    db.refresh(bank)
    return bank


def get_bank_by_id(db: Session, bank_id: int) -> Optional[Bank]:
    return db.query(Bank).filter(Bank.id == bank_id).first()


def get_all_banks(db: Session) -> List[Bank]:
    return db.query(Bank).all()

    