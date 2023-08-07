from fastapi import FastAPI, status, HTTPException, Request
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

     # Create the new response format
    response = {
        "data": {
            "id": id,
            "content": todo.content
        },
        "response_code": 201,
        "response_message": "success"
    }
    # return the id
    return response


@app.get("/todo/{id}")
def read_todo(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo with id
    todo = session.query(TodoClass).get(id)

    session.close()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"todo item with this id{id} not found")
    # return {f"read todo item with id {todo.id} and task: {todo.content} and timestamp {todo.created_at}"}
    return todo



@app.put("/todo/{id}")
async def update_todo(id: int, request: Request):
    # Get the JSON data from the request body
    data = await request.json()
    content = data.get("content")

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
            status_code=status.HTTP_404_NOT_FOUND, detail=f"todo item with id {id} not found")

    # Create the new response format
    response = {
        "data": {
            "id": id,
            "content": content
        },
        "response_code": 200,
        "response_message": "success"
    }
    return response

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
        response = {
            "response_code": 404,
            "response_message": "Todo not found!"
        }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= response)
    return None


@app.get("/todo")
def get_all_todo():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo with id
    todo = session.query(TodoClass).all()

    session.close()

    return todo
