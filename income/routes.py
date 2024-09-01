from typing import Union
from fastapi import APIRouter
from income.schemas import Income

router = APIRouter(
    tags=["Income"]
)


@router.post("/income/new")
def create_new_income(income: Income):
    return {"message": "Income created successfully"}