from fastapi import FastAPI
from income import models
from income.routes import router as income_router
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(income_router)
