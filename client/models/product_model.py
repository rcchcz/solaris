from sqlalchemy import Column, Integer, String, Numeric
from shared.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Numeric)
    image = Column(String(50))
    brand = Column(String(50))
    title = Column(String(50))
    review_score = Column(Numeric)
    clients = relationship('Client', secondary='client_product', back_populates='favorite_products')
