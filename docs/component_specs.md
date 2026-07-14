# Component Specs - moodverse

Specs for the components I personally owned. Each follows the same structure: purpose, interface contract, behavior, edge cases & error handling, invariants, and a test plan sketch. Teammate-owned components (the Genius lyrics pipeline, model fine-tuning) are referenced only where they touch these interfaces.

**Components:**
1. [Frontend Application (UI)](#1-frontend-application-ui)
2. [API Client Layer (`src/api/index.js`)](#2-api-client-layer-srcapiindexjs)
3. [`/classify` Endpoint & Model Serving](#3-classify-endpoint--model-serving)

---

## 1. Frontend Application (UI)

### 1.1 Purpose

The entire user-facing surface: capture input via two modes, orchestrate the backend calls, and render classification results.

### 1.2 Structure

React + Vite, styled with Tailwind CSS.

- **Branding/layout** — "moodverse" wordmark ("mood" regular, "verse" italic) in DM Serif Display; tagline; neutral dark background with a purple accent (`#7F77DD`) reserved for primary actions and the top-mood display
- **Input section** (two tabs):
  - *Paste text*: a textarea for lyrics, quotes, or arbitrary text
  - *Look up a song*: song title input (required) beside an optional artist input, with the hint "Adding an artist helps find the right song."
  - A single **Classify mood** button serves both tabs
- **Results view** — rendered below the input after classification:
  - `DETECTED MOOD`: top mood in large DM Serif Display, purple
  - Confidence chip (e.g., "75% confidence")
  - For song lookups: resolved song title and artist, right-aligned, so users can verify the match
  - `MOOD BREAKDOWN`: one horizontal bar per mood, sorted descending by probability, with percentage labels; the top mood's bar in the accent purple
  - Lyrics toggle to expand/collapse the fetched lyrics
  - "Try Another" button which gives a clean-slate UI
- **State handling** — loading state while requests are in flight; distinct error states (see 1.4)

### 1.3 Behavior

- *Paste text* flow: validate non-empty -> `classifyMood(text)` -> render results
- *Song lookup* flow: validate non-empty title -> `fetchLyrics(title, artist)` -> display resolved song -> `classifyMood(lyrics)` -> render results
- Orchestration of the two-call chain is deliberately client-side (see design doc §7.5)
- Switching tabs preserves each tab's input; results correspond to the most recent classification

### 1.4 Edge Cases & Error Handling

| Case | Behavior |
|---|---|
| Empty textarea / empty title | Blocked client-side; no network call made |
| `/lyrics` returns 404 | "Song not found" state; suggest adding or correcting the artist |
| Backend unreachable / request fails | Error state with retry affordance; input preserved |
| Slow response | Loading indicator persists; button disabled to prevent duplicate submissions |
| Ambiguous title, no artist given | Resolved title/artist shown with results — the user can catch a wrong match |
| Very long pasted text | Sent as-is; truncation happens server-side at tokenization (documented, not hidden) |

### 1.5 Invariants

- No network call is ever made with empty/whitespace-only input
- Rendered percentages always come from the `/classify` response so the frontend never computes or normalizes probabilities
- The Classify button is disabled while any request is in flight (no overlapping submissions)
- The results view always reflects the most recent completed classification, never a stale one

### 1.6 Test Plan Sketch

- **Unit:** tab switching preserves inputs; empty-input validation blocks submission; mood bars render sorted with correct widths/labels from a fixture response
- **Integration (mocked API layer):** happy-path paste flow; happy-path song flow including intermediate resolved-song render; 404 path shows song-not-found; failure path shows error + retry
- **Manual/demo:** slow-network simulation for loading states; long-lyric songs; wrong-song match caught via displayed metadata

---

## 2. API Client Layer (`src/api/index.js`)

### 2.1 Purpose

A single module isolating every network call behind two functions. Components import functions, never `fetch`. This was the seam that made mock-first development work: the module shipped with mock implementations returning contract-shaped data, and swapping to the live backend was a one-file change with zero component edits.

### 2.2 Interface Contract

```js
fetchLyrics(title: string, artist?: string)
  -> Promise<{ lyrics: string, title: string, artist: string }>
  // resolved title/artist from Genius, not the raw user input
  // throws/rejects with a typed "not found" error on 404

classifyMood(text: string)
  -> Promise<{
      mood: string,            // "Happy" | "Sad" | "Angry" | "Relaxed"
      confidence: number,      // probability of the top mood, 0–1
      probabilities: {         // full distribution over all four moods
        happy: number, sad: number, angry: number, relaxed: number
      }
    }>
```

Both functions target the FastAPI server on `localhost:8000` (`POST /lyrics`, `POST /classify`, JSON bodies).

### 2.3 Behavior

- Serializes arguments to the request shape; parses and returns the response body
- Maps HTTP failures to a small error taxonomy the UI can branch on:
  - `NOT_FOUND` — `/lyrics` 404
  - `SERVER_ERROR` — 5xx from either endpoint
  - `NETWORK_ERROR` — fetch rejection / unreachable backend
- Contains no UI logic, no state, no retries — retry policy is a UI decision

### 2.4 Edge Cases

- Omitted `artist` -> sent as absent/null, matching the backend's optional field
- Non-JSON error responses -> coerced into `SERVER_ERROR` rather than throwing a parse error at the caller
- The mock implementations return realistic contract-shaped data (including a plausible probability distribution) so UI development exercised the same code paths as production

### 2.5 Invariants

- This module is the **only** place in the frontend that performs network I/O
- Return shapes match the backend contract exactly — no renaming, reshaping, or normalization in transit (the contract is the contract)
- Errors surfaced to callers are always from the defined taxonomy, never raw fetch exceptions

### 2.6 Test Plan Sketch

- **Unit (mocked `fetch`):** request bodies match the contract for both functions, with and without `artist`; 404 -> `NOT_FOUND`; 5xx -> `SERVER_ERROR`; rejection -> `NETWORK_ERROR`; response fields pass through unmodified
- **Contract check:** mock implementations validated against the same shape assertions as live responses — if the mocks drift from the contract, tests fail

---

## 3. `/classify` Endpoint & Model Serving

### 3.1 Purpose

Serve mood classification over HTTP from the fine-tuned DistilBERT model. Built in two phases against a frozen contract: a **mock** returning fixed contract-shaped output (unblocking all frontend work), then the **real implementation** performing model inference — with no frontend changes at swap time.

### 3.2 Interface Contract

```
POST /classify
Content-Type: application/json

Request:  { "text": "<lyrics or arbitrary text>" }

200:      {
            "mood": "Happy",
            "confidence": 0.75,
            "probabilities": { "happy": 0.75, "relaxed": 0.14,
                               "angry": 0.06, "sad": 0.05 }
          }
422:      malformed request body (FastAPI/Pydantic validation)
```

`mood` is the argmax of `probabilities`; `confidence` equals the argmax probability. The four keys are always present.

### 3.3 Behavior

**Startup (once per process):**
1. Load the fine-tuned DistilBERT sequence-classification model and its tokenizer from the configured weights path
2. Set the model to eval mode; hold both in module-level memory for the process lifetime
3. If loading fails (missing/corrupt weights), the server fails to start — fail-fast rather than serving a broken endpoint

**Per request:**
1. Validate body via the Pydantic request model
2. Tokenize `text`, truncating to the model's max sequence length
3. Forward pass under `no_grad`; softmax over the four logits
4. Map class indices -> labels (angry, happy, relaxed, sad — fixed by the MoodyLyrics4Q label set)
5. Return top mood, its probability as `confidence`, and the full distribution

### 3.4 Edge Cases & Error Handling

| Case | Behavior |
|---|---|
| Missing/empty `text` | 422 via request validation (frontend also blocks this client-side — defense in both layers) |
| Text longer than max sequence length | Truncated at tokenization; classification reflects the opening section (known limitation, documented in design doc §8 F7/§10) |
| Non-lyric garbage input (e.g., leaked Genius metadata pre-cleanup-fix) | Model classifies it anyway — garbage in, confident garbage out. This surfaced as a real bug and motivated the input-validation improvement in design doc §10 |
| Concurrent requests | Single in-memory model, no queue — acceptable at single-user scale, first bottleneck beyond it |
| Inference exception | 500 with a generic error body; details to server logs |

### 3.5 Invariants

- The model is loaded exactly once per process; no request path ever triggers a model load
- `probabilities` always contains exactly the four moods and sums to ~1.0 (softmax output)
- `mood` is always the argmax of `probabilities`, and `confidence` always equals that maximum — the three fields can never disagree
- The endpoint is stateless and side-effect-free: identical input -> identical output for a given weights file; nothing is persisted
- The response shape is identical between the mock and real implementations (this is what made the swap invisible to the frontend)

### 3.6 Test Plan Sketch

- **Unit:** softmax mapping — given fixed logits, response has correct argmax `mood`, matching `confidence`, all four keys; probabilities sum to about 1.0 
- **Endpoint (FastAPI TestClient):** valid request -> 200 with contract shape; empty/missing `text` -> 422; oversized text -> 200 (truncation is silent, not an error)
- **Contract regression:** the same shape assertions run against both mock and real implementations — the test suite *is* the contract
- **Smoke:** obviously-moody fixtures (an upbeat verse, a bleak verse) produce sensible top moods — not a correctness proof, but a wiring check that catches label-index mismatches immediately

---

*See the [System Design Doc](design_doc.md) for architecture, data flow, decisions/tradeoffs, and failure-mode analysis across the full system.*