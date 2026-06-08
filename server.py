import sys
from pathlib import Path

# need so we can see imports that happen in models/
sys.path.insert(0, str(Path(__file__).parent / "models"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from genius_fetcher import get_lyrics_for_classifier
from predictor import MoodPredictor

# the actual model file and the object 
MODEL_PATH = Path(__file__).parent / "models" / "experiments" / "best"
predictor = MoodPredictor.from_bert(str(MODEL_PATH))

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
    text: str


@app.post("/lyrics")
def get_lyrics(req: SongRequest):
    result = get_lyrics_for_classifier(req.title, req.artist)
    if not result:
        raise HTTPException(status_code=404, detail="Song not found")
    return result


@app.post("/classify")
def classify(req: ClassifyRequest):
    mood = predictor.predict(req.text)
    scores = predictor.predict_proba(req.text)
    return {
        "mood": mood,
        "confidence": scores[mood],
        "scores": scores,
    }
