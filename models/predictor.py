"""
predictor.py — clean interface for Person 4 to consume
No ML knowledge required on their end; just load and call.

Usage:
    from exported.predictor import MoodPredictor

    # Baseline (sklearn)
    p = MoodPredictor.from_sklearn("exported/baseline.joblib")

    # BERT
    p = MoodPredictor.from_bert("experiments/bert/best")

    # Then identically for both:
    p.predict("I wanna dance all night")          # -> "happy"
    p.predict_proba("I wanna dance all night")    # -> {"angry": 0.03, "happy": 0.87, ...}
"""

from pathlib import Path
from labels import ID2LABEL, LABEL_NAMES


class MoodPredictor:
    def __init__(self, predict_fn, predict_proba_fn):
        # Internal: store callables so both backends look identical from outside
        self._predict_fn      = predict_fn
        self._predict_proba_fn = predict_proba_fn

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_sklearn(cls, model_path):
        """Load a joblib-serialized sklearn pipeline (baseline or any sklearn model)."""
        import joblib
        model = joblib.load(model_path)

        def predict_fn(text):
            idx = model.predict([text])[0]
            return ID2LABEL[idx]

        def predict_proba_fn(text):
            probs = model.predict_proba([text])[0]
            return {ID2LABEL[i]: float(p) for i, p in enumerate(probs)}

        return cls(predict_fn, predict_proba_fn)

    @classmethod
    def from_bert(cls, model_dir):
        """Load a saved HuggingFace model + tokenizer from a directory."""
        import torch
        import numpy as np
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model     = AutoModelForSequenceClassification.from_pretrained(model_dir)
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        def _run(text):
            inputs = tokenizer(text, return_tensors="pt", truncation=True,
                               max_length=256, padding=True)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            with torch.no_grad():
                logits = model(**inputs).logits
            return torch.softmax(logits, dim=-1).cpu().numpy()[0]

        def predict_fn(text):
            probs = _run(text)
            return ID2LABEL[int(np.argmax(probs))]

        def predict_proba_fn(text):
            probs = _run(text)
            return {ID2LABEL[i]: float(p) for i, p in enumerate(probs)}

        return cls(predict_fn, predict_proba_fn)

    # ------------------------------------------------------------------
    # Public API — this is what Person 4 calls
    # ------------------------------------------------------------------

    def predict(self, text: str) -> str:
        """Return the single most likely mood label."""
        return self._predict_fn(text)

    def predict_proba(self, text: str) -> dict:
        """Return a dict of {mood: probability} for all 4 classes."""
        return self._predict_proba_fn(text)