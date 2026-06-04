from __future__ import annotations

import re
from statistics import pstdev

# Heuristic weights tuned for a conservative baseline:
# lexical uniformity has strongest influence, then sentence-length regularity,
# then repeated adjacent tokens; the scale maps to a 0-100 output range.
UNIQUE_WEIGHT = 45
BURSTINESS_WEIGHT = 35
REPETITION_WEIGHT = 20
SCORE_SCALE = 1.4


def _clamp_percentage(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def estimate_ai_percentage(text: str) -> dict:
    content = (text or "").strip()
    if not content:
        return {
            "ai_generated_percentage": 0.0,
            "reasoning": "No content found in uploaded file.",
        }

    words = re.findall(r"\b\w+\b", content.lower())
    sentences = [s.strip() for s in re.split(r"[.!?]+", content) if s.strip()]
    if not words:
        return {
            "ai_generated_percentage": 0.0,
            "reasoning": "No valid text tokens found in uploaded file.",
        }

    unique_ratio = len(set(words)) / max(len(words), 1)
    sentence_lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
    if not sentence_lengths:
        sentence_lengths = [len(words)]
    # Higher sentence-length variation usually indicates more human-like writing.
    burstiness = pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0
    consecutive_duplicates = (
        sum(1 for first, second in zip(words, words[1:]) if first == second)
        if len(words) > 1
        else 0
    )
    repetition_ratio = consecutive_duplicates / max(len(words), 1)

    # Weighted heuristic: lower lexical diversity, lower burstiness, and higher repetition
    # increase the estimated probability of AI-generated text.
    score = (
        (1 - unique_ratio) * UNIQUE_WEIGHT
        + (1 / (1 + burstiness)) * BURSTINESS_WEIGHT
        + repetition_ratio * REPETITION_WEIGHT
    ) * SCORE_SCALE

    percentage = _clamp_percentage(score)
    return {
        "ai_generated_percentage": percentage,
        "reasoning": (
            "Heuristic estimate based on lexical variety, sentence burstiness, and repetition patterns."
        ),
    }
