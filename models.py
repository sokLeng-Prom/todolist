from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime
from database import Base

class TodoClass(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)