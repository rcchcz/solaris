from shared.database import Base
from sqlalchemy import Column, Integer, String

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(25))