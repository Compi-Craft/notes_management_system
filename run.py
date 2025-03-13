import uvicorn
from notes_management import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
