from shared.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())