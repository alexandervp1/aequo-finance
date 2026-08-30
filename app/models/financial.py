##Tables Structure for database

from datetime import datetime, timezone
import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.models.base import base

#Defining to restrict transactions to 2 types only.

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = relationship("Transaction", back_populates="owner")

class transaction(base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey="user.id", nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
