from fastapi import HTTPException
from notes_management import client

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def summarize_note_content(content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Summarize note:\n" + content])
    summary = response.text
    if not summary:
        raise HTTPException(status_code=500, detail="Gemini API returned an empty summary")

    return summary