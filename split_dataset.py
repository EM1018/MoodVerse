import csv
import pandas as pd
import random
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    df = pd.read_csv("./data/cano_with_lyrics.csv")

    # 80/10/10 split
    train, dev_and_test = train_test_split(df, test_size=0.2, stratify=df["mood"], random_state=16)
    dev, test = train_test_split(dev_and_test, test_size=0.5, stratify=dev_and_test["mood"], random_state=16)

    train.to_csv("./data/train_with_lyrics.csv", index=False)
    dev.to_csv("./data/dev_with_lyrics.csv", index=False)
    test.to_csv("./data/test_with_lyrics.csv", index=False)
