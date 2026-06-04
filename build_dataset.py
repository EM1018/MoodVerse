import csv

from genius_fetcher import get_lyrics_for_classifier

if __name__ == "__main__":
    missing_lyrics = []
    with open("./data/cano_clean.csv", "r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter=",")
        next(reader)  # Skip header
        with open("./data/cano_with_lyrics.csv", "w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["title", "artist", "lyrics", "mood"])
            count = 0
            for row in reader:
                print(f"\r{((count+1)/2000)*100:.2f}%", end="")
                title, artist, mood = row[2], row[1], row[3]
                info = get_lyrics_for_classifier(title, artist)
                if info is None:
                    missing_lyrics.append((title, artist, mood))
                    count += 1
                    continue
                _, _, lyrics = info.values()
                writer.writerow([title, artist, lyrics, mood])
                count += 1
    with open("./data/missing_lyrics.txt", "w", encoding="utf-8") as f:
        for title, artist, mood in missing_lyrics:
            f.write(f"{title} by {artist} with mood {mood}\n")
