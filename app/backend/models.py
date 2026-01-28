from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.backend.database import Base


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


class ProfitHistory(Base):
    __tablename__ = "profit_history"

    id = Column(Integer, primary_key=True)
    total_purchase = Column(Float)
    total_sales = Column(Float)
    profit = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
