from pydantic import BaseModel

class TodoRequest(BaseModel):
    content: str