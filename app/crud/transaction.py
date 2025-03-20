from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate

async def create_transaction(db: AsyncSession, transaction: TransactionCreate, user_id: int) -> Transaction:
    db_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        category=transaction.category,
        type=transaction.type,
        date=transaction.date,
        user_id=user_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalar_one_or_none()

async def get_user_transactions(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_user_transactions_by_type(db: AsyncSession, user_id: int, transaction_type: TransactionType, skip: int = 0, limit: int = 100) -> List[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id, Transaction.type == transaction_type).offset(skip).limit(limit))
    return result.scalars().all()

async def update_transaction(db: AsyncSession, transaction_id: int, transaction: TransactionUpdate) -> Optional[Transaction]:
    db_transaction = await get_transaction(db, transaction_id)
    if not db_transaction:
        return None
    
    update_data = transaction.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def delete_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    transaction = await get_transaction(db, transaction_id)
    if transaction:
        await db.delete(transaction)
        await db.commit()
    return transaction 