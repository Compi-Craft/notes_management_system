"Analytics route"

from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notes_management import SessionLocal
from notes_management.models import Note
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

router = APIRouter()

def get_db():
    "Get db function"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_and_tokenize(text: str):
    "Removes stop words from analytics"
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return cleaned_tokens

@router.get("/analytics", response_model=dict)
def get_notes_analytics(db: Session = Depends(get_db)):
    "Get notes function"
    notes = db.query(Note).all()

    if not notes:
        raise HTTPException(status_code=404, detail="No notes found")

    note_data = [{"id": note.id, "title": note.title, "content": note.content} for note in notes]

    df = pd.DataFrame(note_data)

    df['word_count'] = df['content'].apply(lambda x: len(clean_and_tokenize(x)))
    total_word_count = int(df['word_count'].sum())

    average_note_length = float(df['word_count'].mean())

    all_tokens = [token for content in df['content'] for token in clean_and_tokenize(content)]
    word_counts = Counter(all_tokens)
    most_common_words = word_counts.most_common(10)

    df['content_length'] = df['content'].apply(len)
    longest_notes = df.nlargest(3, 'content_length')[['id', 'title', 'content_length']]
    shortest_notes = df.nsmallest(3, 'content_length')[['id', 'title', 'content_length']]

    df['word_count'] = df['word_count'].astype(int)
    longest_notes = longest_notes.astype(str)
    shortest_notes = shortest_notes.astype(str)

    analytics = {
        "total_word_count": total_word_count,
        "average_note_length": average_note_length,
        "most_common_words": most_common_words,
        "top_3_longest_notes": longest_notes.to_dict(orient='records'),
        "top_3_shortest_notes": shortest_notes.to_dict(orient='records')
    }

    return analytics
