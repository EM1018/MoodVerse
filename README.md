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
Developed a two-model pipeline for 4-class mood classification (happy, sad, angry, relaxed) using the dataset provided by Tyler. The pipeline consists of a TF-IDF + Logistic Regression baseline and a fine-tuned DistilBERT model. Both models are wrapped behind a unified `MoodPredictor` interface consumed by the backend. DistilBERT was selected as the deployed model based on validation macro F1.

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
Purpose: TF-IDF + Logistic Regression baseline classifier.
Builds a sklearn pipeline combining TF-IDF vectorization and logistic regression for 4-class mood classification. Key hyperparameters:
* `ngram_range=(1,2)` — uses unigrams and bigrams as features to capture phrase-level context
* `max_features=30000` — limits vocabulary to the 30,000 most frequent n-grams to reduce noise
* `sublinear_tf=True` — applies log normalization to term frequencies, preventing repeated words (e.g. chorus repetition) from dominating
* `min_df=2` — ignores terms appearing in only one document
* `C=1.0` — logistic regression regularization strength
* `class_weight="balanced"` — adjusts weights inversely proportional to class frequency as a safeguard against imbalance
* `solver=lbfgs`, `multi_class=multinomial` — solves the 4-class problem jointly rather than one-vs-rest

### bert_finetune.py (Ethan)
Purpose: Fine-tunes DistilBERT (`distilbert-base-uncased`) for 4-class mood classification.
Uses the HuggingFace `Trainer` API with early stopping based on validation macro F1. Key hyperparameters:
* `learning_rate=3e-5` — standard range for transformer fine-tuning; higher values destabilize pretrained weights
* `batch_size=8` — small batches increase gradient updates per epoch, beneficial for small datasets
* `max_length=256` — truncates lyrics to 256 tokens; captures most mood signal without the memory cost of full 512-token inputs
* `weight_decay=0.01` — L2 regularization on transformer weights to reduce overfitting
* `warmup_ratio=0.1` — linearly increases learning rate over the first 10% of steps to stabilize early training
* `early_stopping_patience=2` — halts training if validation macro F1 does not improve for 2 consecutive epochs; consistently triggered at epoch 2
RoBERTa (`roberta-base`) was also evaluated but underperformed DistilBERT (0.588 vs 0.637 val macro F1), likely due to higher overfitting risk from increased model size on a 1600-sample training set.
 
### predictor.py (Ethan)
Purpose: Unified inference wrapper for the backend to consume.
Exposes `MoodPredictor.from_bert(model_dir)` and `MoodPredictor.from_sklearn(model_path)` constructors. Both backends implement the same interface:
* `predict(text)` — returns the single most likely mood label as a string
* `predict_proba(text)` — returns a dict of `{mood: probability}` for all 4 classes, used by the frontend mood visualization

### evaluate.py (Ethan)
Purpose: Shared evaluation utilities.
Provides per-class F1 reporting, confusion matrix generation, and JSON experiment logging. All training runs are logged to `models/experiments/` for comparison.
 
### train.py (Ethan)
Purpose: End-to-end training pipeline.
Runs baseline and DistilBERT sequentially, compares validation macro F1, and writes the winning model path to `exported/winner.txt`.

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

Evaluation metric: **macro F1** (preferred over accuracy for multi-class classification as it treats all classes equally regardless of support).
 
| Model | Val Macro F1 | Test Macro F1 |
|---|---|---|
| TF-IDF + Logistic Regression (baseline) | 0.591 | 0.570 |
| DistilBERT (fine-tuned) | **0.637** | 0.570 |

 
**Per-class test F1 (DistilBERT):**
 
| Class | Precision | Recall | F1 |
|---|---|---|---|
| Angry | 0.71 | 0.78 | 0.74 |
| Happy | 0.65 | 0.68 | 0.67 |
| Sad | 0.49 | 0.50 | 0.50 |
| Relaxed | 0.41 | 0.35 | 0.38 |
 
DistilBERT was selected as the deployed model. Both models converge to the same test performance (0.57 macro F1), suggesting the performance ceiling is dataset size and the inherent ambiguity of lyrics-only classification rather than model capacity.
 
**Key failure modes identified:**
* **Musical irony** — songs like *Hey Ya* (Outkast) and *Born in the USA* (Springsteen) have lyrics that contradict the intended emotional register. A lyrics-only model cannot resolve this without audio features.
* **Relaxed/Sad confusion** — both moods share low-energy, introspective vocabulary. The distinction is largely carried by tempo and instrumentation, not words. This is reflected in Relaxed having the lowest per-class F1 (0.38) across both models.
* **Genre-specific language** — hip-hop and trap lyrics express emotion through culturally coded language that diverges from the training distribution (e.g. *Drugs You Should Try It* by Travis Scott is classified as happy despite being a melancholic track).
**Proposed improvements:**
* Multimodal input combining lyrics with Spotify audio features (`valence`, `energy`) to resolve mood ambiguity
* Chorus-only classification rather than full lyrics to reduce noise from contrasting verses
* Additional training data, particularly for the Relaxed class

---

## References

[1] Çano, E., & Morisio, M. (2019). Word Embeddings for Sentiment Analysis: A Comprehensive Empirical Survey. ArXiv, abs/1902.00753.