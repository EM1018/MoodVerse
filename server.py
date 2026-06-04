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


class ClassifyRequest(BaseModel): 
    text : str 


@app.post("/lyrics")
def get_lyrics(req: SongRequest):
    result = get_lyrics_for_classifier(req.title, req.artist)
    if not result:
        raise HTTPException(status_code=404, detail="Song not found")
    return result


@app.post("/classify")
def classify(req: ClassifyRequest):
    # replace with actual model call and return results
    # using dummy data for now
    return {
        "mood": "melancholic",
        "confidence": 0.87,
        "scores": {
            "melancholic": 0.87,
            "sad": 0.61,
            "nostalgic": 0.44,
            "romantic": 0.19,
            "angry": 0.08,
            "happy": 0.03,
        },
    }
