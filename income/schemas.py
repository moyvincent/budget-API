from pydantic import BaseModel


class IncomeBase(BaseModel):
    income_name: str
    income_type: int
    income_amount: float

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int

    class Config:
        orm_mode = True