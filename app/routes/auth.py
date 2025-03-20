from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import get_settings
from app.core.deps import authenticate_user, get_current_user
from app.core.security import create_access_token, get_password_hash
from app.db.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema, UserCreate
import logging

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.email, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserSchema)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    try:
        # Check if user exists
        result = await db.execute(select(User).filter(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        
        # Create new user
        now = datetime.utcnow()
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
            created_at=now,
            updated_at=now
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Convert SQLAlchemy model to dictionary
        user_dict = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at or now,
            "updated_at": user.updated_at or now
        }
        
        # Create and return Pydantic model
        return UserSchema(**user_dict)
    except HTTPException as he:
        await db.rollback()
        raise he
    except Exception as e:
        await db.rollback()
        logger.error(f"Error during user registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Error during user registration: {str(e)}"
        ) 