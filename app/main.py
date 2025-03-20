from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routes import auth, users, transactions

settings = get_settings()

app = FastAPI(
    title="Budget Calculator API",
    description="API for managing personal budget and expenses",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(transactions.router, prefix=settings.API_V1_STR, tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to Budget Calculator API"} 