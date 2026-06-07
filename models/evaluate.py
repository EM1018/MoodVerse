"""
evaluate.py — shared evaluation logic and experiment logging
"""

import json
import datetime
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt

from labels import LABEL_NAMES


def full_report(y_true, y_pred, model_name="model"):
    """Print and return a full classification report."""
    print(f"\n=== {model_name} ===")
    print(classification_report(y_true, y_pred, target_names=LABEL_NAMES, zero_division=0))
    return classification_report(y_true, y_pred, target_names=LABEL_NAMES,
                                  output_dict=True, zero_division=0)


def plot_confusion_matrix(y_true, y_pred, model_name="model", save_path=None):
    """
    Plot and optionally save confusion matrix.
    Key pairs to watch: relaxed↔sad (low-energy confusion), angry↔happy (high-energy confusion).
    """
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABEL_NAMES)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"Confusion Matrix — {model_name}")
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        print(f"Confusion matrix saved → {save_path}")
    else:
        plt.show()
    plt.close()
    return cm


def log_run(model_name, params, metrics, experiments_dir="experiments"):
    """
    Save a JSON record of every run for easy comparison later.
    File: experiments/{model_name}_{date}.json
    """
    Path(experiments_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    run = {
        "timestamp": timestamp,
        "model": model_name,
        "params": params,
        "metrics": metrics,
    }
    fname = Path(experiments_dir) / f"{model_name}_{timestamp[:10]}.json"
    # If a file for today already exists, append a counter
    counter = 1
    while fname.exists():
        fname = Path(experiments_dir) / f"{model_name}_{timestamp[:10]}_{counter}.json"
        counter += 1

    with open(fname, "w") as f:
        json.dump(run, f, indent=2)
    print(f"Run logged → {fname}")


def compare_runs(experiments_dir="experiments"):
    """Print a summary table of all logged runs, sorted by macro F1."""
    runs = []
    for fp in Path(experiments_dir).glob("*.json"):
        with open(fp) as f:
            run = json.load(f)
        macro_f1 = (
            run["metrics"].get("f1_macro")
            or run["metrics"].get("macro avg", {}).get("f1-score", 0)
        )
        runs.append((macro_f1, run["model"], run["timestamp"][:10], fp.name))

    if not runs:
        print("No runs logged yet.")
        return

    runs.sort(reverse=True)
    print(f"\n{'F1 Macro':>10}  {'Model':<20}  {'Date':<12}  File")
    print("-" * 65)
    for f1, model, date, fname in runs:
        print(f"{f1:>10.4f}  {model:<20}  {date:<12}  {fname}")