from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.transaction import Income, Expense
from app.db.database import Base, engine, async_session

settings = get_settings()

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    
def create_first_superuser() -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@example.com").first()
        if not user:
            user = User(
                email="admin@example.com",
                name="Admin",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True,
                is_active=True
            )
            db.add(user)
            db.commit()
            print("Superuser created successfully!")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Creating first superuser...")
    create_first_superuser() 