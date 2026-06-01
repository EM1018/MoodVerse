import lyricsgenius

GENIUS_TOKEN = "Veg8X7Xj1-8gdBgERi5UI01EZQTP8Q-5ZBd5tfn_gAMQcQORbVFmCv5TwZZwl3kB"
genius = lyricsgenius.Genius(GENIUS_TOKEN, timeout=15)

def fetch_lyrics(song_title, artist=None):
    try:
        song = genius.search_song(song_title, artist or "", get_full_info=False)
        if not song:
            return None
        return {
            "title": song.title,
            "artist": song.artist,
            "lyrics": song.lyrics
        }
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None

if __name__ == "__main__":
    result = fetch_lyrics("Bohemian Rhapsody", "Queen")
    if result:
        print(f"{result['title']} by {result['artist']}")
        print(result['lyrics'][:300])
    else:
        print("Not found")