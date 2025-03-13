import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from notes_management.models import Base
from google import genai




load_dotenv()

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = "sqlite:///./notes.db"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

client = genai.Client(api_key=GEMINI_API_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from notes_management import routes
