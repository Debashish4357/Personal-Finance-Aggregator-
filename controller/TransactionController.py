# controller/TransactionController.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schema.models import Transaction, TransactionType, TransactionCategory, RegisteredUser


def create_transaction(
    db: Session,
    from_account_id: int,
    transaction_type: TransactionType,
    amount: float,
    category: TransactionCategory,
    balance_after_transaction: float,
    to_account_id: Optional[int] = None,
    transaction_date: Optional[datetime] = None
) -> Transaction:

    if transaction_date is None:
        transaction_date = datetime.utcnow()

    # Fetch user accounts correctly using `id`
    from_account = db.query(RegisteredUser).filter(RegisteredUser.id == from_account_id).first()

    to_account = None
    if to_account_id is not None:
        to_account = db.query(RegisteredUser).filter(RegisteredUser.id == to_account_id).first()

    # Validate existence
    if from_account is None:
        raise ValueError("Sender account not found")

    if to_account_id and to_account is None:
        raise ValueError("Receiver account not found")

    # Update balances
    from_account.account_balance -= amount

    if to_account:
        to_account.account_balance += amount

    # Create transaction entry
    tx = Transaction(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        transaction_date=transaction_date,
        balance_after_transaction=from_account.account_balance
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)

    return tx



def get_transaction_by_id(db: Session, tx_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.id == tx_id).first()


def get_transactions_by_account(
    db: Session,
    account_id: int,
    limit: int = 50,
    skip: int = 0
) -> List[Transaction]:
    return (
        db.query(Transaction)
        .filter(Transaction.from_account_id == account_id)
        .order_by(Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )