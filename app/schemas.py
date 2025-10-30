from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True