from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


db_url = "sqlite:///todooo.db"
engine = create_engine(db_url)

#base class, use it before calling function
Base = declarative_base()

class TodoClass(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)

#The ToDo database model tells the database how to set up the todos table. The ToDo pydantic model defines the acceptable input data format for creating a new todo item.
# Create the database
Base.metadata.create_all(engine)