# routes/AlertRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.AlertController import (
    get_alerts_by_user, get_alert_by_id, mark_alert_as_read,
    mark_all_alerts_as_read, delete_alert
)
from schema.models import AlertType
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/alerts", tags=["Alerts"])

class AlertResponse(BaseModel):
    id: int
    user_id: int
    budget_id: Optional[int]
    alert_type: AlertType
    message: str
    is_read: int
    created_at: str

    class Config:
        from_attributes = True


@router.get("/user/{user_id}", response_model=List[AlertResponse])
def get_user_alerts(user_id: int, unread_only: bool = False, db: Session = Depends(get_db)):
    alerts = get_alerts_by_user(db, user_id, unread_only)
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    return alert


@router.post("/{alert_id}/read", response_model=AlertResponse)
def mark_read(alert_id: int, db: Session = Depends(get_db)):
    alert = mark_alert_as_read(db, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    db.commit()
    return alert


@router.post("/user/{user_id}/read-all")
def mark_all_read(user_id: int, db: Session = Depends(get_db)):
    count = mark_all_alerts_as_read(db, user_id)
    db.commit()
    return {"message": f"Marked {count} alerts as read"}


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_route(alert_id: int, db: Session = Depends(get_db)):
    if not delete_alert(db, alert_id):
        raise HTTPException(404, "Alert not found")
    db.commit()
    return None

