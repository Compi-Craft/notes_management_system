import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from notes_management import app, SECRET_KEY
from notes_management.models import User, Note, NoteVersion
from sqlalchemy.orm import Session
from notes_management import SessionLocal, pwd_context
import jwt

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    print("Cleaning")
    db.query(User).delete()
    db.query(Note).delete()
    db.query(NoteVersion).delete()
    db.commit()
    db.close()

def create_test_user(db: Session):
    hashed_password = pwd_context.hash("testpassword")
    user = User(username="testuser", password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm="HS256")

@pytest.fixture(scope="module")
def test_user(db):
    return create_test_user(db)

@pytest.fixture(scope="module")
def auth_headers(test_user):
    token = create_test_token(test_user.username)
    return {"Authorization": f"Bearer {token}"}

def test_create_user(client, db):
    response = client.post("/users/", json={"username": "newuser", "password": "newpassword"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "newuser"

def test_login(client, test_user):
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_create_note(client, auth_headers):
    with patch("notes_management.routes.summarize_note_content", return_value="Mocked Summary"):
        response = client.post("/notes/", json={"title": "Test Note", "content": "Test Content"}, headers=auth_headers)
        assert response.status_code == 200
        assert "id" in response.json()
        assert response.json()["summary"] == "Mocked Summary"

def test_read_note(client, db, auth_headers):
    note = Note(title="Existing Note", content="Content", user_id=2, summary="Summary")
    db.add(note)
    db.commit()
    db.refresh(note)
    response = client.get(f"/notes/{note.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Existing Note"

def test_update_note(client, db, auth_headers):
    note = db.query(Note).filter_by(user_id=2).first()
    with patch("notes_management.routes.summarize_note_content", return_value="Updated Summary"):
        response = client.put(f"/notes/{note.id}", json={"title": "Updated Title", "content": "Updated Content"}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["summary"] == "Updated Summary"

def test_delete_note(client, db, auth_headers):
    note = db.query(Note).filter_by(user_id=2).first()
    response = client.delete(f"/notes/{note.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted successfully"

def test_get_notes_analytics(client, db, auth_headers):
    note_1 = Note(title="Note 1", content="This is the content of the first note.", user_id=2)
    note_2 = Note(title="Note 2", content="The second note's content is here.", user_id=2)
    note_3 = Note(title="Note 3", content="Short content.", user_id=2)
    db.add_all([note_1, note_2, note_3])
    db.commit()

    response = client.get("/analytics", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert "total_word_count" in data
    assert "average_note_length" in data
    assert "most_common_words" in data
    assert "top_3_longest_notes" in data
    assert "top_3_shortest_notes" in data

    assert len(data["top_3_longest_notes"]) == 3
    assert len(data["top_3_shortest_notes"]) == 3
    
def test_update_note_and_create_version(client, db, auth_headers):
    note = Note(title="Original Note", content="This is the original note content.", user_id=2)
    db.add(note)
    db.commit()
    db.refresh(note)

    update_data = {"title": "Updated Note", "content": "This is the updated note content."}
    response = client.put(f"/notes/{note.id}", json=update_data, headers=auth_headers)
    
    assert response.status_code == 200
    updated_note = response.json()
    assert updated_note["title"] == "Updated Note"
    assert updated_note["content"] == "This is the updated note content."

    versions = db.query(NoteVersion).filter_by(note_id=note.id).all()
    assert len(versions) == 1
    assert versions[0].title == "Original Note"
    assert versions[0].content == "This is the original note content."

def test_get_note_versions(client, db, auth_headers):
    note = Note(title="Original Note", content="This is the original note content.", user_id=2)
    db.add(note)
    db.commit()
    db.refresh(note)

    update_data = {"title": "Updated Note", "content": "This is the updated note content."}
    client.put(f"/notes/{note.id}", json=update_data, headers=auth_headers)

    response = client.get(f"/notes/{note.id}/versions", headers=auth_headers)

    assert response.status_code == 200
    versions = response.json()
    assert len(versions) > 0
    assert versions[0]["title"] == "Original Note"
    assert versions[0]["content"] == "This is the original note content."
    assert "created_at" in versions[0]
