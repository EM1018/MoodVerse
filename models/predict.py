"""
predict.py — test both models side by side on any lyrics
Run interactively:         python predict.py
Run from a lyrics file:    python predict.py lyrics.txt
"""

import sys
from predictor import MoodPredictor

BERT_DIR = "experiments/bert/best"
BASELINE = "exported/baseline.joblib"


def print_comparison(baseline_probs, bert_probs):
    models = [("Baseline", baseline_probs), ("BERT", bert_probs)]
    moods = ["angry", "happy", "relaxed", "sad"]

    print(f"\n{'Mood':<12}", end="")
    for name, _ in models:
        print(f"  {name:<18}", end="")
    print()
    print("-" * 50)

    for mood in moods:
        print(f"  {mood:<10}", end="")
        for _, probs in models:
            p = probs[mood]
            bar = "█" * int(p * 20)
            print(f"  {p:.3f} {bar:<20}", end="")
        print()

    print()
    for name, probs in models:
        label = max(probs, key=probs.get)
        print(f"  {name:<10} → {label.upper()}")
    print()


def classify(baseline, bert, lyrics):
    baseline_probs = baseline.predict_proba(lyrics)
    bert_probs     = bert.predict_proba(lyrics)
    print_comparison(baseline_probs, bert_probs)


def main():
    print("Loading models...")
    baseline = MoodPredictor.from_sklearn(BASELINE)
    print("  Baseline loaded.")
    bert = MoodPredictor.from_bert(BERT_DIR)
    print("  BERT loaded.\n")

    # File mode: python predict.py lyrics.txt
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, encoding="utf-8") as f:
            lyrics = f.read().strip()
        print(f"Classifying: {path}\n")
        classify(baseline, bert, lyrics)
        return

    # Interactive mode
    print("Type 'quit' to exit.")
    print("Tip: press Enter TWICE on a blank line to classify.\n")

    while True:
        print("Paste lyrics:")
        lines = []
        consecutive_blanks = 0
        while True:
            line = input()
            if line.lower() == "quit":
                return
            if line == "":
                consecutive_blanks += 1
                if consecutive_blanks >= 2:
                    break
                lines.append("")
            else:
                consecutive_blanks = 0
                lines.append(line)

        lyrics = "\n".join(lines).strip()
        if not lyrics:
            continue
        classify(baseline, bert, lyrics)


if __name__ == "__main__":
    main()