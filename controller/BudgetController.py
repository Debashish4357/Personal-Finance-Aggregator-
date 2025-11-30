# controller/BudgetController.py
from typing import List, Optional
from sqlalchemy.orm import Session
from schema.models import Budget, TransactionCategory


def create_budget(
    db: Session,
    user_id: int,
    category: TransactionCategory,
    monthly_limit: float
) -> Budget:
    budget = Budget(
        user_id=user_id,
        category=category,
        monthly_limit=monthly_limit,
        current_spent=0.0
    )
    db.add(budget)
    db.flush()
    db.refresh(budget)
    return budget


def get_budget_by_id(db: Session, budget_id: int) -> Optional[Budget]:
    return db.query(Budget).filter(Budget.id == budget_id).first()


def get_budgets_by_user(db: Session, user_id: int) -> List[Budget]:
    return db.query(Budget).filter(Budget.user_id == user_id).all()


def update_budget_spent(db: Session, budget_id: int, amount: float) -> Optional[Budget]:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        return None
    budget.current_spent += amount
    db.flush()
    db.refresh(budget)
    return budget


def reset_monthly_budget(db: Session, budget_id: int) -> Optional[Budget]:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget:
        budget.current_spent = 0.0
        db.flush()
        db.refresh(budget)
    return budget