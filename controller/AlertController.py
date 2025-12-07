# controller/AlertController.py
from typing import List, Optional
from sqlalchemy.orm import Session
from schema.models import Alert, AlertType, User, Budget

def create_alert(
    db: Session,
    user_id: int,
    alert_type: AlertType,
    message: str,
    budget_id: Optional[int] = None
) -> Alert:
    alert = Alert(
        user_id=user_id,
        budget_id=budget_id,
        alert_type=alert_type,
        message=message,
        is_read=0
    )
    db.add(alert)
    db.flush()
    db.refresh(alert)
    return alert


def get_alert_by_id(db: Session, alert_id: int) -> Optional[Alert]:
    return db.query(Alert).filter(Alert.id == alert_id).first()


def get_alerts_by_user(db: Session, user_id: int, unread_only: bool = False) -> List[Alert]:
    query = db.query(Alert).filter(Alert.user_id == user_id)
    if unread_only:
        query = query.filter(Alert.is_read == 0)
    return query.order_by(Alert.created_at.desc()).all()


def mark_alert_as_read(db: Session, alert_id: int) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_read = 1
        db.flush()
        db.refresh(alert)
    return alert


def mark_all_alerts_as_read(db: Session, user_id: int) -> int:
    count = db.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.is_read == 0
    ).update({"is_read": 1})
    db.flush()
    return count


def delete_alert(db: Session, alert_id: int) -> bool:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        return True
    return False


def check_and_generate_budget_alerts(db: Session, user_id: int) -> List[Alert]:
    """Check budgets and generate alerts at 80% and 100% thresholds"""
    generated_alerts = []
    
    # Get all budgets for the user
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    
    for budget in budgets:
        if budget.monthly_limit <= 0:
            continue
            
        percentage = (budget.current_spent / budget.monthly_limit) * 100
        
        # Check for 100% threshold
        if percentage >= 100:
            # Check if alert already exists for this budget at 100%
            existing_alert = db.query(Alert).filter(
                Alert.budget_id == budget.id,
                Alert.alert_type == AlertType.BUDGET_100_PERCENT,
                Alert.is_read == 0
            ).first()
            
            if not existing_alert:
                message = f"Budget exceeded! {budget.category.value} category has reached {percentage:.1f}% (₹{budget.current_spent:.2f} / ₹{budget.monthly_limit:.2f})"
                alert = create_alert(
                    db,
                    user_id,
                    AlertType.BUDGET_100_PERCENT,
                    message,
                    budget.id
                )
                generated_alerts.append(alert)
        
        # Check for 80% threshold
        elif percentage >= 80:
            # Check if alert already exists for this budget at 80%
            existing_alert = db.query(Alert).filter(
                Alert.budget_id == budget.id,
                Alert.alert_type == AlertType.BUDGET_80_PERCENT,
                Alert.is_read == 0
            ).first()
            
            if not existing_alert:
                message = f"Budget warning! {budget.category.value} category has reached {percentage:.1f}% (₹{budget.current_spent:.2f} / ₹{budget.monthly_limit:.2f})"
                alert = create_alert(
                    db,
                    user_id,
                    AlertType.BUDGET_80_PERCENT,
                    message,
                    budget.id
                )
                generated_alerts.append(alert)
    
    return generated_alerts


def check_overall_balance_limit_alert(db: Session, user_id: int, total_balance: float) -> Optional[Alert]:
    """Check overall balance limit and generate alert if exceeded"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.overall_balance_limit:
        return None
    
    if total_balance > user.overall_balance_limit:
        # Check if alert already exists
        existing_alert = db.query(Alert).filter(
            Alert.user_id == user_id,
            Alert.alert_type == AlertType.OVERALL_BALANCE_LIMIT,
            Alert.is_read == 0
        ).first()
        
        if not existing_alert:
            message = f"Overall balance limit exceeded! Current balance: ₹{total_balance:.2f}, Limit: ₹{user.overall_balance_limit:.2f}"
            return create_alert(
                db,
                user_id,
                AlertType.OVERALL_BALANCE_LIMIT,
                message
            )
    
    return None

