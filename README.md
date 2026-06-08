# MoodVerse - CSE 143 Final Project - Team 16

## Tasks per person:
* Tyler - Data collection & preprocessing
* Ethan - Model training & evaluation
* Nuha - API integration & backend & poster/slideshow
* Elian - Frontend & UI

---

## How to run
*someone fill this in*

---

## Team Discussion - Implementation Decisions

**Tyler (Data):**
*To be filled in by Tyler.*

**Ethan (Model):**
*To be filled in by Ethan.*

**Nuha (API Integration):**
Built the Genius lyrics pipeline using the `lyricsgenius` library. Given a song title and artist, it fetches the lyrics, cleans them up (removes section headers like `[Intro]`, contributor info, and other Genius metadata), and returns plain text ready to be classified. Also set up a FastAPI backend with two endpoints, one to fetch lyrics by song title and one to run mood classification, connected to the frontend.

**Elian (Frontend):**
*To be filled in by Elian.*

---

## File Descriptions

### genius_fetcher.py (Nuha)
Purpose: Fetches and cleans song lyrics from the Genius API
Functions:
* `fetch_lyrics(song_title, artist)` - searches Genius and returns title, artist, and cleaned lyrics
* `clean_lyrics(lyrics)` - strips `[Intro]`/`[Verse]` headers and Genius contributor metadata
* `get_lyrics_for_classifier(song_title, artist)` - wrapper that returns `{"title", "artist", "text"}` ready for the model

### server.py (Nuha)
Purpose: FastAPI backend connecting the frontend to the lyrics fetcher and classifier
Endpoints:
* `POST /lyrics` - takes `{title, artist}`, returns cleaned lyrics or 404 if not found
* `POST /classify` - takes `{text}`, returns mood prediction and confidence scores

### build_dataset.py (Tyler)
*To be filled in by Tyler.*

### split_dataset.py (Tyler)
*To be filled in by Tyler.*

### baseline.py (Ethan)
*To be filled in by Ethan.*

### bert_finetune.py (Ethan)
*To be filled in by Ethan.*

### frontend/ (Elian)
*To be filled in by Elian.*

---

## Results

*To be filled in by Ethan.*
