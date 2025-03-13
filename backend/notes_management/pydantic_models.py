from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class NoteCreateRequest(BaseModel):
    title: str
    content: str
    
class NoteUpdateRequest(BaseModel):
    title: str
    content: str
    
class NoteVersionResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime