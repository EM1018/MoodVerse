# Mood-Based Lyric and Quote Classifier

## Overview

We plan to build a mood-based text classifier that categorizes song lyrics and quotes into emotional categories (happy, sad, angry, romantic, melancholic, etc.). Users can input text (in the form of lyrics/quotes) and receive a mood classification. This can be useful for playlist curation, quote discovery, or understanding the emotional tone of lyrics in general.

**Why this matters:** Music and quotes are deeply personal. Understanding the emotional content helps people find songs that match their mood or discover quotes that resonate with how they're feeling, or even just for fun!

---

## What We'll Build

A text classification system with:

- **Input:** Song lyrics, quotes, or even short text passages
- **Output:** Mood classification (e.g., "happy," "sad," "angry," "romantic," "nostalgic")

**Possible features:**

- Spotify API integration: For a given song title, fetch lyrics and automatically classify the mood, then suggest similar mood-based songs
- Build a simple web interface where users can paste lyrics/quotes
- Visualize confusion between mood categories (which moods get mixed up?)

---

## Dataset

We'll use existing datasets and APIs:

- **MoodyLyrics Dataset** - A dataset of lyrics labeled with moods like happy, sad, angry, relaxed (Hu & Downie, 2010) [1]
- **Spotify API** - To fetch song metadata, audio features, and link to lyrics sources
- **Genius API** - For fetching song lyrics
- Potentially augment with quote datasets from Goodreads or manually labeled examples
- **Language:** We'll mostly work with English lyrics and quotes for simplicity

---

## Related Work

**Emotion detection in song lyrics:**

- Hu & Downie (2010) created the MoodyLyrics dataset with 5 mood categories and showed that lyrics alone can predict song mood with reasonable accuracy [1]
- Zaanen & Kanters (2010) used sentiment analysis techniques on Dutch song lyrics to classify emotional content [2]

**Music emotion recognition:**

- Kim et al. (2010) combined audio features and lyric features for emotion classification, and found that lyrics contribute significantly to perceived emotion [3]
- Spotify uses similar approaches internally for playlist curation (e.g., mood-based playlists like "Chill" or "Happy Hits")

---

## Success/Performance Metrics

- **Accuracy:** How often does our model correctly classify the mood?
- **Confusion matrix:** Which moods get confused? (melancholic vs sad, romantic vs happy)
- **Qualitative evaluation:** Test on songs we know well. Do the classifications feel right?
- **Comparison:** How do different methods (bag-of-words, etc.) perform?

---

## Challenges

- **Ambiguity:** Some lyrics express mixed emotions or shift moods mid-song
- **Data imbalance:** Some moods (happy/sad) might have more examples than others
- **API rate limits:** Spotify and Genius have request limits we'll need to work around

---

## References

[1] Hu, X., & Downie, J. S. (2010). Improving mood classification in music digital libraries by combining lyrics and audio. *Proceedings of the 10th annual joint conference on Digital libraries*.

[2] van Zaanen, M., & Kanters, P. (2010). Automatic mood classification using TF*IDF based on lyrics. *11th International Society for Music Information Retrieval Conference (ISMIR 2010)*.

[3] Kim, Y., Schmidt, E. M., Migneco, R., Morton, B. G., Richardson, P., Scott, J., ... & Turnbull, D. (2010). Music emotion recognition: A state of the art review. *Proceedings of ISMIR*.