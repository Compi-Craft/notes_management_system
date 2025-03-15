"Pydantic models"

from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    "User creation class"
    username: str
    password: str

class NoteCreateRequest(BaseModel):
    "Note creation class"
    title: str
    content: str

class NoteUpdateRequest(BaseModel):
    "Note update class"
    title: str
    content: str

class NoteVersionResponse(BaseModel):
    "Note version class"
    id: int
    title: str
    content: str
    created_at: datetime
