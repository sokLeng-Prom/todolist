from fastapi import FastAPI, status
from database import Base, engine, TodoClass
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

 
#initialize app
app = FastAPI()

class TodoRequest(BaseModel):
    content: str

#define end point
@app.get("/")
def root():
    return {"todoo"}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model with the current timestamp
    tododb = TodoClass(content=todo.content, created_at=datetime.utcnow())

    # add it to the session and commit it
    session.add(tododb)
    session.commit()

    # grab the id given to the object from the database
    id = tododb.id

    # close the session
    session.close()

    # return the id
    return f"created todo item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    #get the todo with id
    todo = session.query(TodoClass).get(id)

    session.close()
    
    return {f"read todo item with id {todo.id} and task: {todo.content} and timestamp {todo.created_at}"}

@app.put("/todo/{id}")
def update_todo(id: int):
    return {"update todo"}

@app.delete("/todo/{id}")
def delete_todo(id:int):
    return {"delete todo item"}

@app.get("/todo")
def get_all_todo(id: int):
    return {"read all todo item"}

