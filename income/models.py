from sqlalchemy import Column, Float, Integer, String
from database import Base

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True)
    income_name = Column(String, index=True)
    income_type = Column(Integer, index=True)
    income_amount = Column(Float, index=True)
