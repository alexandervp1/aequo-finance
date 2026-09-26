##Tables Structure for database

from datetime import datetime, timezone
import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base

#Defining to restrict transactions to 2 types only.

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, nullable=False, index=True)

    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    description = Column(String, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="transactions")

#Saving charts into database

class Candle(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    interval = Column(String(20), nullable=False, index=True)
    timestamp = Column(datetime, nullable=False, index=True)

    open = Column(Numeric(precision=18, scale=8), nullable=False)
    high = Column(Numeric(precision=18, scale=8), nullable=False)
    low = Column(Numeric(precision=18, scale=8), nullable=False)
    close = Column(Numeric(precision=18, scale=8), nullable=False)
    volume = Column(Numeric(precision=24, scale=8), nullable=False)

    # Ensure we never insert duplicate candles for the same symbol + interval + timestamp
    __table_args__ = (
        UniqueConstraint("symbol", "interval", "timestamp", name="uq_symbol_interval_timestamp"),
    )


