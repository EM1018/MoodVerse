# moodverse

A mood classifier for lyrics and text. Paste any text or look up a song title and moodverse predicts the overall emotional tone across happy, sad, agnry, and relaxed moods, using a fine-tuned DistilBERT model, with lyrics fetched from the Genius API.

>**note**: This is a team project built for ucscs CSE143 (NLP). See [My Role](#my-role).

moodverse classifying "Can't stop the feeling" by Justin Timberlake:

![alt text](image.png)
---

## What It Does

- **Two input modes** — paste raw text (lyrics, quotes, anything), or look up a song by title with an optional artist field for disambiguation
- **Mood classification** — a DistilBERT model fine-tuned on the MoodyLyrics4Q dataset predicts a probability for each of four moods
- **Full mood breakdown** — the UI displays the top mood with a confidence chip, plus a bar for every mood's probability (e.g. Happy 75%, Relaxed 14%, Angry 6%, Sad 5%)
- **Live lyrics retrieval** — song lookups pull real lyrics from the Genius API, cleaned of contributor/translation metadata before classification


## Running Locally

moodverse is a local tool

**System**: 
- Python 3.9+
- Node.js 18+
- npm

**Python dependencies**:

Install via `pip install -r requirements.txt` 


**Model**: 

The best/ folder (DistilBERT checkpoint) placed at models/experiments/best/ — not included in the repo due to size, reach out if needed

**API Key**:

This project requires a Genius API token.

1. Get a free token at https://genius.com/api-clients
2. Create a file called `.env` at root directory
3. Add the following line:
   GENIUS_TOKEN=your_token_here



## My Role

My personal contributions:

- **Entire frontend** — the React + Vite app end to end: tabbed input UI, results view (including analyzed lyrics), mood-breakdown bars, loading and error states, and the visual design (DM Serif Display wordmark, purple accent system)
- **API contract design** — defined the request/response shapes both endpoints serve to the frontend, and built the isolated API client layer (`src/api/index.js`) with mock implementations so the UI could be built and demoed before any backend existed
- **`/classify` endpoint** — wrote the original mock endpoint that unblocked frontend development, then replaced it with the real implementation: loading the fine-tuned DistilBERT model at server startup and serving per-mood probabilities per request
- **frontend and backend integration** — wired the frontend to both live endpoints and handled the integration edge cases (song not found, slow responses, empty input)


## The Model

- **Base:** DistilBERT, fine-tuned for sequence classification (fine-tuned by a teammate) 
- **Dataset:** [MoodyLyrics4Q](https://softeng.polito.it/erion/research.html) (Erion Çano) which was chosen because, for copyright reasons, no public dataset ships raw lyrics; MoodyLyrics4Q provides mood-labeled song references (**model fined-tuned with only about 2,000 songs**)
- **Mood classes:** Angry, Happy, Relaxed, Sad
- **Training:** 3 epochs with train/validation/test splits
- **Serving:** loaded once into memory at FastAPI startup. There is no per-request model loading, so inference latency stays low after boot


## Documentation

- [System Design Doc](docs/design_doc.md) — problem statement, requirements, architecture, data flow, decisions and tradeoffs
- [Component Specs](docs/component_specs.md) — interface contracts, edge cases, invariants, and test plans for the components I owned


## Tech Stack

**Frontend:** React, Vite, Tailwind CSS 

**Backend:** FastAPI, Pydantic, Uvicorn 

**ML:** DistilBERT (Hugging Face Transformers), PyTorch 

**External:** Genius API