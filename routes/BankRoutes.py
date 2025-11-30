
    # routes/BankRoutes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from controller.BankController import create_bank, get_bank_by_id, get_all_banks
from pydantic import BaseModel

router = APIRouter(prefix="/banks", tags=["Banks"])

class BankCreate(BaseModel):
    bank_name: str

class BankResponse(BaseModel):
    id: int
    bank_name: str

    class Config:
        from_attributes = True


@router.post("/", response_model=BankResponse, status_code=status.HTTP_201_CREATED)
def add_bank(bank: BankCreate, db: Session = Depends(get_db)):
    new_bank = create_bank(db, bank.bank_name)
    db.commit()
    return new_bank


@router.get("/", response_model=list[BankResponse])
def list_banks(db: Session = Depends(get_db)):
    return get_all_banks(db)


@router.get("/{bank_id}", response_model=BankResponse)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    bank = get_bank_by_id(db, bank_id)
    if not bank:
        raise HTTPException(404, "Bank not found")
    return bank