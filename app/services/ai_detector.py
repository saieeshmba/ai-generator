from __future__ import annotations

import re
from statistics import pstdev


def _safe_percentage(value: float) -> float:
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
    sentence_lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences] or [len(words)]
    burstiness = pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0
    repeated_pairs = len(words) - len(set(zip(words, words[1:]))) if len(words) > 1 else 0
    repetition_ratio = repeated_pairs / max(len(words), 1)

    score = (
        (1 - unique_ratio) * 45
        + (1 / (1 + burstiness)) * 35
        + repetition_ratio * 20
    ) * 1.4

    percentage = _safe_percentage(score)
    return {
        "ai_generated_percentage": percentage,
        "reasoning": (
            "Heuristic estimate based on lexical variety, sentence burstiness, and repetition patterns."
        ),
    }
