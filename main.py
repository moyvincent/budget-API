from fastapi import FastAPI
from income.routes import router as income_router

app = FastAPI()
app.include_router(income_router)