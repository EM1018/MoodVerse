import lyricsgenius
import re

GENIUS_TOKEN = "Veg8X7Xj1-8gdBgERi5UI01EZQTP8Q-5ZBd5tfn_gAMQcQORbVFmCv5TwZZwl3kB"
genius = lyricsgenius.Genius(GENIUS_TOKEN, timeout=15)

def clean_lyrics(lyrics):
    if "Read More" in lyrics:
        lyrics = lyrics[lyrics.index("Read More") + len("Read More"):]
    lyrics = re.sub(r'\[.*?\]', '', lyrics)
    lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)
    return lyrics.strip()

def fetch_lyrics(song_title, artist=None):
    if not song_title or not song_title.strip():
        return None
    try:
        song = genius.search_song(song_title, artist or "", get_full_info=False)
        if not song:
            return None
        return {
            "title": song.title,
            "artist": song.artist,
            "lyrics": clean_lyrics(song.lyrics)
        }
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None

def get_lyrics_for_classifier(song_title, artist=None):
    result = fetch_lyrics(song_title, artist)
    if not result:
        return None
    return {
        "title": result["title"],
        "artist": result["artist"],
        "text": result["lyrics"]
    }
