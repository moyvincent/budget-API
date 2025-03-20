from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_current_active_superuser
from app.core.security import get_password_hash
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from sqlalchemy import select
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    # Convert SQLAlchemy model to dictionary
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "created_at": current_user.created_at or datetime.utcnow(),
        "updated_at": current_user.updated_at or datetime.utcnow()
    }
    return UserSchema(**user_dict)

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.email is not None:
        current_user.email = user_in.email
    
    await db.commit()
    await db.refresh(current_user)
    
    # Convert SQLAlchemy model to dictionary
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "created_at": current_user.created_at or datetime.utcnow(),
        "updated_at": current_user.updated_at or datetime.utcnow()
    }
    return UserSchema(**user_dict)

@router.get("", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> List[UserSchema]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return [
        UserSchema(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at or datetime.utcnow(),
            updated_at=user.updated_at or datetime.utcnow()
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert SQLAlchemy model to dictionary
    user_dict = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "created_at": user.created_at or datetime.utcnow(),
        "updated_at": user.updated_at or datetime.utcnow()
    }
    return UserSchema(**user_dict) 