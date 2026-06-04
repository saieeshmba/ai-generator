from __future__ import annotations


SEMINAR_KEYWORDS = {
    "seminar",
    "speaker",
    "speakers",
    "agenda",
    "topic",
    "venue",
    "time",
    "schedule",
    "registration",
}


def detect_intent(text: str) -> str:
    lowered = (text or "").lower()
    if any(keyword in lowered for keyword in SEMINAR_KEYWORDS):
        return "seminar_details"
    return "general_query"
