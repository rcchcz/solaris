from shared.database import Base
from sqlalchemy import Column, ForeignKey, Integer

# Association table Client-Product
class ClientProduct(Base):
    __tablename__ = 'client_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column('client_id', Integer, ForeignKey('client.id'))
    product_id = Column('product_id', Integer, ForeignKey('product.id'))

