import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import get_settings
from app.db.database import Base, engine, async_session
from app.models.user import User
from app.models.transaction import Income, Expense

settings = get_settings()

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def main() -> None:
    asyncio.run(init_db())

if __name__ == "__main__":
    main() 