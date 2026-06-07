"""
train.py — entry point for all training runs
Runs baseline first, then optionally BERT. Saves the winner to exported/.

Usage:
    python train.py --train data/train.csv --val data/val.csv
    python train.py --train data/train.csv --val data/val.csv --skip_bert
    python train.py --train data/train.csv --val data/val.csv --test data/test.csv
"""

import argparse
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import classification_report

from labels import LABEL2ID, LABEL_NAMES
from baseline import train as train_baseline
from bert_finetune import train as train_bert
from evaluate import full_report, plot_confusion_matrix, compare_runs
# from models.exported.predictor import MoodPredictor


def get_preds_sklearn(model, csv_path):
    df = pd.read_csv(csv_path)
    X = df["lyrics"].tolist()
    y_true = df["mood"].str.lower().map(LABEL2ID).tolist()
    y_pred = model.predict(X)
    return y_true, list(y_pred)


def get_preds_bert(trainer, csv_path):
    import numpy as np
    df = pd.read_csv(csv_path)
    from datasets import Dataset
    from bert_finetune import tokenize_batch
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    ds = Dataset.from_dict({"lyrics": df["lyrics"].tolist(),
                             "label": df["mood"].str.lower().map(LABEL2ID).tolist()})
    ds = ds.map(lambda x: tokenize_batch(x, tokenizer), batched=True)
    preds_out = trainer.predict(ds)
    y_pred = np.argmax(preds_out.predictions, axis=-1).tolist()
    y_true = preds_out.label_ids.tolist()
    return y_true, y_pred


def main(args):
    print("\n" + "="*60)
    print("STAGE 1: Baseline (TF-IDF + Logistic Regression)")
    print("="*60)
    baseline_model, baseline_report = train_baseline(
        args.train, args.val,
        save_path="exported/baseline.joblib",
        C=args.C,
    )
    baseline_f1 = baseline_report["macro avg"]["f1-score"]
    print(f"\nBaseline macro F1: {baseline_f1:.4f}")

    if args.test:
        print("\n--- Baseline on test set ---")
        y_true, y_pred = get_preds_sklearn(baseline_model, args.test)
        full_report(y_true, y_pred, model_name="Baseline (test)")
        plot_confusion_matrix(y_true, y_pred, model_name="Baseline",
                              save_path="experiments/baseline_confusion.png")

    if args.skip_bert:
        print("\nSkipping BERT. Baseline is the exported model.")
        compare_runs()
        return

    print("\n" + "="*60)
    print("STAGE 2: DistilBERT Fine-tuning")
    print("="*60)
    trainer, tokenizer = train_bert(
        args.train, args.val,
        output_dir="experiments/bert",
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
    )

    # Compare on val set
    y_true, y_pred = get_preds_bert(trainer, args.val)
    bert_report = full_report(y_true, y_pred, model_name="BERT (val)")
    bert_f1 = bert_report["macro avg"]["f1-score"]
    print(f"\nBERT macro F1: {bert_f1:.4f}")

    if args.test:
        print("\n--- BERT on test set ---")
        y_true_t, y_pred_t = get_preds_bert(trainer, args.test)
        full_report(y_true_t, y_pred_t, model_name="BERT (test)")
        plot_confusion_matrix(y_true_t, y_pred_t, model_name="BERT",
                              save_path="experiments/bert_confusion.png")

    # ------------------------------------------------------------------
    # Pick winner
    # ------------------------------------------------------------------
    print("\n" + "="*60)
    if bert_f1 > baseline_f1:
        print(f"Winner: BERT ({bert_f1:.4f} > {baseline_f1:.4f})")
        print("Exported model: experiments/bert/best  (use MoodPredictor.from_bert)")
        Path("exported/winner.txt").write_text("bert:experiments/bert/best")
    else:
        print(f"Winner: Baseline ({baseline_f1:.4f} >= {bert_f1:.4f})")
        print("Exported model: exported/baseline.joblib  (use MoodPredictor.from_sklearn)")
        Path("exported/winner.txt").write_text("sklearn:exported/baseline.joblib")

    compare_runs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train",      required=True,  help="Path to train CSV")
    parser.add_argument("--val",        required=True,  help="Path to validation CSV")
    parser.add_argument("--test",       default=None,   help="Path to test CSV (optional)")
    parser.add_argument("--skip_bert",  action="store_true", help="Only run baseline")
    # Baseline hyperparams
    parser.add_argument("--C",          type=float, default=1.0)
    # BERT hyperparams
    parser.add_argument("--epochs",     type=int,   default=3)
    parser.add_argument("--batch_size", type=int,   default=16)
    parser.add_argument("--lr",         type=float, default=2e-5)
    args = parser.parse_args()
    main(args)