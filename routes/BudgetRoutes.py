# routes/BudgetRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.BudgetController import (
    create_budget, get_budgets_by_user, get_budget_by_id,
    update_budget_spent, reset_monthly_budget
)
from schema.models import TransactionCategory
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/budgets", tags=["Budgets"])

class BudgetCreate(BaseModel):
    user_id: int
    category: TransactionCategory
    monthly_limit: float

class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category: TransactionCategory
    monthly_limit: float
    current_spent: float

    class Config:
        from_attributes = True

class OverallBalanceLimitUpdate(BaseModel):
    user_id: int
    overall_balance_limit: float


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def set_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    new_budget = create_budget(db, budget.user_id, budget.category, budget.monthly_limit)
    db.commit()
    return new_budget


@router.get("/user/{user_id}", response_model=List[BudgetResponse])
def get_user_budgets(user_id: int, db: Session = Depends(get_db)):
    return get_budgets_by_user(db, user_id)


@router.post("/{budget_id}/reset")
def reset_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = reset_monthly_budget(db, budget_id)
    if not budget:
        raise HTTPException(404, "Budget not found")
    db.commit()
    return {"message": "Budget reset successfully", "budget": budget}


@router.post("/overall-balance-limit")
def set_overall_balance_limit(limit_data: OverallBalanceLimitUpdate, db: Session = Depends(get_db)):
    from controller.userController import get_user_by_id, update_user
    user = get_user_by_id(db, limit_data.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    user = update_user(db, limit_data.user_id, {"overall_balance_limit": limit_data.overall_balance_limit})
    db.commit()
    return {"message": "Overall balance limit set successfully", "user_id": user.id, "overall_balance_limit": user.overall_balance_limit}


@router.get("/overall-balance-limit/{user_id}")
def get_overall_balance_limit(user_id: int, db: Session = Depends(get_db)):
    from controller.userController import get_user_by_id
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {"user_id": user.id, "overall_balance_limit": user.overall_balance_limit}


@router.post("/trigger-sync")
def trigger_manual_sync(db: Session = Depends(get_db)):
    """Manually trigger sync workflow"""
    from services.sync_service import full_sync_workflow
    try:
        full_sync_workflow()
        return {"message": "Sync completed successfully"}
    except Exception as e:
        raise HTTPException(500, f"Sync failed: {str(e)}")