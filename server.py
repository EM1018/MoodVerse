from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from genius_fetcher import get_lyrics_for_classifier

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SongRequest(BaseModel):
    title: str
    artist: str = None

@app.post("/lyrics")
def get_lyrics(req: SongRequest):
    result = get_lyrics_for_classifier(req.title, req.artist)
    if not result:
        raise HTTPException(status_code=404, detail="Song not found")
    return result
