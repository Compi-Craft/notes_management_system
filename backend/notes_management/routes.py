"Routes module"

from typing import List
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from notes_management import app, SessionLocal, oauth2_scheme, pwd_context, SECRET_KEY, ALGORITHM
from notes_management.models import User, Note, NoteVersion
from notes_management.pydantic_models import UserCreate, NoteCreateRequest, NoteUpdateRequest, NoteVersionResponse
from notes_management.gemini_api import summarize_note_content

from notes_management.analytics import router as analytics_router

app.include_router(analytics_router)

def get_db():
    "Get db function"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    "Gets current user by token"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    check_user = db.query(User).filter(User.username == user.username).first()
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}

@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes/", response_model=dict)
async def create_note(note: NoteCreateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_note = Note(title=note.title, content=note.content, user_id=user.id)
    
    summary = await summarize_note_content(note.content)
    new_note.summary = summary
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "summary": new_note.summary
    }


@app.get("/notes/{note_id}", response_model=dict)
def read_note(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": note.id, "title": note.title, "content": note.content, "summary": note.summary, "updated_at": note.updated_at}

@app.put("/notes/{note_id}", response_model=dict)
async def update_note(note_id: int, note: NoteUpdateRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    note_db = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
    if note_db is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note_version = NoteVersion(note_id=note_db.id, title=note_db.title, content=note_db.content, summary = note_db.summary)
    db.add(note_version)
    note_db.title = note.title
    note_db.content = note.content
    note_db.summary = await summarize_note_content(note.content)
    
    db.commit()
    db.refresh(note_db)
    
    return {
        "id": note_db.id,
        "title": note_db.title,
        "content": note_db.content,
        "summary": note_db.summary
    }


@app.delete("/notes/{note_id}", response_model=dict)
def delete_note(note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    "Delete note route"
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

@app.get("/notes/{note_id}/versions", response_model=List[NoteVersionResponse])
def get_note_versions(note_id: int,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    "Get note versions route"
    versions = db.query(NoteVersion).join(Note).filter(NoteVersion.note_id == note_id, 
        Note.user_id == user.id).all()
    return [{"id": v.id, "title": v.title, "content": v.content,
             "summary": v.summary, "created_at": v.created_at} for v in versions]
