# MoodVerse - CSE 143 Final Project - Team 16

## Tasks per person:
* Tyler - Data collection & preprocessing
* Ethan - Model training & evaluation
<<<<<<< Updated upstream
* Nuha - API integration & backend & poster/slideshow
* Elian - Frontend & UI
=======
* Nuha - API integration & backend
* Elian - Frontend/Bit of Backend & UI/UX
>>>>>>> Stashed changes

---

## How to run
* To run the server: `python3 -m uvicorn server:app`
* To run the frontend (Vite dev server using React): 
    - `cd frontend` 
    - `npm run dev` 

note: this is a development server, not a production server

---

## Team Discussion - Implementation Decisions

**Tyler (Data):**
*To be filled in by Tyler.*

**Ethan (Model):**
*To be filled in by Ethan.*

**Nuha (API Integration):**
Built the Genius lyrics pipeline using the `lyricsgenius` library. Given a song title and artist, it fetches the lyrics, cleans them up (removes section headers like `[Intro]`, contributor info, and other Genius metadata), and returns plain text ready to be classified. Also set up a FastAPI backend with two endpoints, one to fetch lyrics by song title and one to run mood classification, connected to the frontend.

**Elian (Frontend/Backend):**
Built out the UI and UX for the application using React for implementing logic and building components and Vite to host. Provided the backend with the data that it needed to fulfill it's response via `fetch()`. Integrated the trained model into the system. API contribution by implementing the call to the trained model in the API endpoint `/classify`.

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
`public/src/api/index.js`
The bridge between the frontend and backend
Functions: 
* `fetchLyrics(title, artist)`: uses fetch() to make a request to the backend, passing in both the title and artist. Both parameters are used to obtain the lyrics of a song title. Note that the artist parameter is made optional for the client.

* `classifyMood(text)`: uses fetch() to make a request to the backend, passing in only text (lyrics), which is used as input for the model to perform it's classification.

`public/src/components`
The components rendered on the client side. 
Files:
* `MoodBars.jsx`: renders the moods that the model predicted in percentages. 
* `ResultsView.jsx`: renders the primary result mood that had the highest percentage out of all the moods.
* `TabInput.jsx`: renders the input text box for either text only mode or song title and optinally artist. 

`public/src/App.jsx`:
Responsible for displaying each of the components that are defined in `public/src/components`. Passes the needed data for `index.js` to pass to the backend.

### `classify(req: ClassifyRequest)` in `server.py` (Elian)
Provides the input from the frontend to the model so that it can classify the data from the client, using `predict` to obtain the primary mood of the text/lyrics, and `predict_proba` to obtain the dictionary of scores that were assigned to the labels (moodes) by the model.


---

## Results

*To be filled in by Ethan.*
