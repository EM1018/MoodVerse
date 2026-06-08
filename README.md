# MoodVerse - CSE 143 Final Project - Team 16

## Tasks per person:
* Tyler - Data collection & preprocessing
* Ethan - Model training & evaluation
* Nuha - API integration & backend & poster/slideshow
* Elian - Frontend/Bit of Backend & UI/UX

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
Sourced, cleaned, and constructed the dataset. Our dataset was constructed based on the MoodyLyrics4Q by Erion Çano [1]. It contains 2000 songs labeled with one of the 4 categories based on Russell's model (happy, sad, angry, relaxed). Dataset was constructed with scripts to avoid unapproved distribution of copyrighted lyrics.

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
Purpose: Gather the lyrics and construct the complete dataset
Reads the song titles and associated artists from the cleaned Çano dataset. Lyrics are fetched using the genius fetcher and saved to `./data/cano_with_lyrics.csv`. Any songs that cannot be found are saved to `./data/missing_lyrics.txt`.


### split_dataset.py (Tyler)
Purpose: Split dataset into train, dev, and test sets.
Uses sklearn's train_test_split to create an 80/10/10 split for the data. Split dataset is stored in `./data/train_with_lyrics.csv`, `./data/dev_with_lyrics.csv`, and `./data/test_with_lyrics.csv`.

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

---

## References

[1] Çano, E., & Morisio, M. (2019). Word Embeddings for Sentiment Analysis: A Comprehensive Empirical Survey. ArXiv, abs/1902.00753.