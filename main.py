from fastapi import FastAPI
from income import models
from income.routes import router as income_router
from database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(income_router)

# Define a list of allowed origins
origins = [
    "http://localhost",
    "http://localhost:3000"  # Adjust as needed for your frontend URL
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
