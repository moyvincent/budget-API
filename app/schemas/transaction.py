from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount (must be greater than 0)")
    description: Optional[str] = Field(None, description="Optional transaction description")
    category: str = Field(..., min_length=1, description="Transaction category")
    type: TransactionType = Field(..., description="Transaction type (income or expense)")
    date: datetime = Field(..., description="Transaction date in ISO format")

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Transaction amount (must be greater than 0)")
    description: Optional[str] = Field(None, description="Optional transaction description")
    category: Optional[str] = Field(None, min_length=1, description="Transaction category")
    type: Optional[TransactionType] = Field(None, description="Transaction type (income or expense)")
    date: Optional[datetime] = Field(None, description="Transaction date in ISO format")

class TransactionInDBBase(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass

class TransactionInDB(TransactionInDBBase):
    pass 