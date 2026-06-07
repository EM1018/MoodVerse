"""
baseline.py — TF-IDF + Logistic Regression classifier
Run directly:  python baseline.py --train data/train.csv --val data/val.csv
"""

import argparse
import json
import joblib
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from labels import LABEL2ID, LABEL_NAMES
from evaluate import log_run


def build_pipeline(C=1.0, max_features=30000, ngram_max=2):
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, ngram_max),
            max_features=max_features,
            sublinear_tf=True,       # log normalization, helps with long lyrics
            strip_accents="unicode",
            min_df=2,                # drop terms appearing in only 1 doc
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=C,
            class_weight="balanced", # compensates if Person 1's data is skewed
            solver="lbfgs",
            
        )),
    ])


def train(train_csv, val_csv, save_path="exported/baseline.joblib", C=1.0):
    train_df = pd.read_csv(train_csv)
    val_df   = pd.read_csv(val_csv)

    # Expect columns: "lyrics", "mood"
    X_train, y_train = train_df["lyrics"].tolist(), train_df["mood"].str.lower().map(LABEL2ID).tolist()
    X_val,   y_val   = val_df["lyrics"].tolist(),   val_df["mood"].str.lower().map(LABEL2ID).tolist()

    model = build_pipeline(C=C)
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    report = classification_report(y_val, preds, target_names=LABEL_NAMES, output_dict=True)
    print(classification_report(y_val, preds, target_names=LABEL_NAMES))

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, save_path)
    print(f"Model saved → {save_path}")

    log_run("baseline", {"C": C, "train_csv": str(train_csv)}, report)
    return model, report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--val",   required=True)
    parser.add_argument("--C",     type=float, default=1.0)
    parser.add_argument("--out",   default="exported/baseline.joblib")
    args = parser.parse_args()
    train(args.train, args.val, save_path=args.out, C=args.C)