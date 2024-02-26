from sqlalchemy import Column, Integer, String, Numeric
from shared.database import Base

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Numeric)
    image = Column(String(50))
    brand = Column(String(50))
    title = Column(String(50))
    review_score = Column(Numeric)
