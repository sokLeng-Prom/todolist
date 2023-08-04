from fastapi import FastAPI, status, HTTPException
from database import engine
from sqlalchemy.orm import Session
from datetime import datetime
from models import TodoClass
from schemas import TodoRequest


# initialize app
app = FastAPI()


# define end point
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

    # get the todo with id
    todo = session.query(TodoClass).get(id)

    session.close()

    if not todo:
        raise HTTPException(
            status_code=404, detail=f"todo item with this id{id} not found")
    # return {f"read todo item with id {todo.id} and task: {todo.content} and timestamp {todo.created_at}"}
    return todo


@app.put("/todo/{id}")
def update_todo(id: int, content: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo with id
    todo = session.query(TodoClass).get(id)

    if todo:
        todo.content = content
        session.commit()

    session.close()
    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(
            status_code=404, detail=f"todo item with id {id} not found")
    return {f"update todo with this item's id{todo.id} and {todo.content} "}


@app.delete("/todo/{id}")
def delete_todo(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo with id
    todo = session.query(TodoClass).get(id)

    # if given id exist, delete from db
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"todo item with id {id} not found")
    return None


@app.get("/todo")
def get_all_todo():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo with id
    todo = session.query(TodoClass).all()

    session.close()

    return todo
