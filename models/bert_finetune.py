"""
bert_finetune.py — DistilBERT fine-tuning for 4-class mood classification
Run directly:  python bert_finetune.py --train data/train.csv --val data/val.csv
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import classification_report

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)
from datasets import Dataset

from labels import LABEL2ID, ID2LABEL, LABEL_NAMES, NUM_LABELS
from evaluate import log_run

# DistilBERT: 40% faster than full BERT, ~2-3% accuracy loss — good starting point.
# Swap to "bert-base-uncased" or "roberta-base" if you want to chase top performance.

# MODEL_NAME = "distilbert-base-uncased"
MODEL_NAME = "bert-base-uncased"
# MODEL_NAME = "roberta-base"

MAX_LENGTH = 256   # 256 tokens covers most lyrics; 512 is overkill and slow


def tokenize_batch(examples, tokenizer):
    return tokenizer(
        examples["lyrics"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    report = classification_report(
        labels, preds,
        target_names=LABEL_NAMES,
        output_dict=True,
        zero_division=0,
    )
    return {
        "accuracy":    report["accuracy"],
        "f1_macro":    report["macro avg"]["f1-score"],
        "f1_angry":    report["angry"]["f1-score"],
        "f1_happy":    report["happy"]["f1-score"],
        "f1_relaxed":  report["relaxed"]["f1-score"],   # watch this one — likely weakest
        "f1_sad":      report["sad"]["f1-score"],
    }


def train(train_csv, val_csv, output_dir="experiments/bert", num_epochs=3, batch_size=16, lr=2e-5):
    train_df = pd.read_csv(train_csv)
    val_df   = pd.read_csv(val_csv)

    # Expect columns: "lyrics", "mood"
    train_df["label"] = train_df["mood"].str.lower().map(LABEL2ID)
    val_df["label"]   = val_df["mood"].str.lower().map(LABEL2ID)

    train_ds = Dataset.from_dict({"lyrics": train_df["lyrics"].tolist(), "label": train_df["label"].tolist()})
    val_ds   = Dataset.from_dict({"lyrics": val_df["lyrics"].tolist(),   "label": val_df["label"].tolist()})

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_ds  = train_ds.map(lambda x: tokenize_batch(x, tokenizer), batched=True)
    val_ds    = val_ds.map(lambda x: tokenize_batch(x, tokenizer),   batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=NUM_LABELS,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 2,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        learning_rate=lr,
        weight_decay=0.01,
        warmup_ratio=0.1,
        logging_dir=f"{output_dir}/logs",
        logging_steps=50,
        report_to="none",   # swap to "wandb" if you set up experiment tracking
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    trainer.train()

    # Save tokenizer alongside model so the predictor can load both from one dir
    best_dir = f"{output_dir}/best"
    trainer.save_model(best_dir)
    tokenizer.save_pretrained(best_dir)
    print(f"Best model saved → {best_dir}")

    # Log final val metrics
    final_metrics = trainer.evaluate()
    log_run("bert", {"model": MODEL_NAME, "epochs": num_epochs, "lr": lr}, final_metrics)

    return trainer, tokenizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train",      required=True)
    parser.add_argument("--val",        required=True)
    parser.add_argument("--epochs",     type=int,   default=3)
    parser.add_argument("--batch_size", type=int,   default=16)
    parser.add_argument("--lr",         type=float, default=2e-5)
    parser.add_argument("--out",        default="experiments/bert")
    args = parser.parse_args()
    train(args.train, args.val, output_dir=args.out, num_epochs=args.epochs,
          batch_size=args.batch_size, lr=args.lr)