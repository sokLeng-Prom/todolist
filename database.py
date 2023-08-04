from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


db_url = "sqlite:///todooo.db"
engine = create_engine(db_url)

#base class, use it before calling function
Base = declarative_base()


#The ToDo database model tells the database how to set up the todos table. The ToDo pydantic model defines the acceptable input data format for creating a new todo item.
# Create the database
Base.metadata.create_all(engine)