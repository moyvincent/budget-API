from typing import List, Union
from fastapi import APIRouter, Depends
from database import SessionLocal
from income import models
from income.schemas import Income, IncomeCreate
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Income"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/income/new")
def create_new_income(income: IncomeCreate, db: Session = Depends(get_db)):
    db_income = models.Income(**income.model_dump())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return {"message": "Income created successfully"}, db_income

@router.get("/income/{income_id}", response_model= Income)
def get_income_by_id(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.id == income_id).first()
    return db_income

@router.get("/incomes/", response_model= List[Income])
def get_all_income(db: Session = Depends(get_db)):
    db_income = db.query(models.Income).all()
    return db_income