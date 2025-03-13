from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

Base = declarative_base()

from pydantic import BaseModel

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

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    notes = relationship("Note", back_populates="user")

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="notes")
    versions = relationship("NoteVersion", back_populates="note", cascade="all, delete-orphan")

class NoteVersion(Base):
    __tablename__ = "note_versions"
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    note = relationship("Note", back_populates="versions")