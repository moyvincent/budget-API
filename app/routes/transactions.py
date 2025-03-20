from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_active_user, get_db
from app.crud.transaction import (
    create_transaction, get_transaction, get_user_transactions,
    get_user_transactions_by_type, update_transaction, delete_transaction
)
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import Transaction as TransactionSchema, TransactionCreate, TransactionUpdate
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])

def convert_to_schema(db_transaction: Transaction) -> TransactionSchema:
    """Convert SQLAlchemy model to Pydantic schema"""
    return TransactionSchema(
        id=db_transaction.id,
        user_id=db_transaction.user_id,
        amount=db_transaction.amount,
        description=db_transaction.description,
        category=db_transaction.category,
        type=db_transaction.type,
        date=db_transaction.date,
        created_at=db_transaction.created_at or datetime.utcnow(),
        updated_at=db_transaction.updated_at
    )

@router.post("", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
async def create_user_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_in: TransactionCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new transaction for current user.
    """
    transaction = await create_transaction(db, transaction_in, current_user.id)
    return convert_to_schema(transaction)

@router.get("", response_model=List[TransactionSchema])
async def read_user_transactions(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    transaction_type: TransactionType = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve transactions for current user.
    """
    if transaction_type:
        transactions = await get_user_transactions_by_type(db, current_user.id, transaction_type, skip=skip, limit=limit)
    else:
        transactions = await get_user_transactions(db, current_user.id, skip=skip, limit=limit)
    return [convert_to_schema(transaction) for transaction in transactions]

@router.get("/{transaction_id}", response_model=TransactionSchema)
async def read_user_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific transaction by ID.
    """
    transaction = await get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return convert_to_schema(transaction)

@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_user_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_id: int,
    transaction_in: TransactionUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a transaction.
    """
    transaction = await get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    transaction = await update_transaction(db, transaction_id, transaction_in)
    return convert_to_schema(transaction)

@router.delete("/{transaction_id}", response_model=TransactionSchema)
async def delete_user_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete a transaction.
    """
    transaction = await get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    transaction = await delete_transaction(db, transaction_id)
    return convert_to_schema(transaction) 