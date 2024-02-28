from typing import Set
from client.models.product_model import Product
from shared.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped

# Association Client-Product
client_product = Table(
    "client_product",
    Base.metadata,
    Column("client", ForeignKey("client.id"), primary_key=True),
    Column("product", ForeignKey("product.id"), primary_key=True),
)

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    fav_products: Mapped[Set[Product]] = relationship(secondary=client_product)