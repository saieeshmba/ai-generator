from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_detects_seminar_intent() -> None:
    response = client.post(
        "/chat",
        json={"question": "Give me seminar details including speaker and schedule"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "seminar_details"
    assert "answer" in payload


def test_chat_general_query_intent() -> None:
    response = client.post("/chat", json={"question": "What is machine learning?"})
    assert response.status_code == 200
    assert response.json()["intent"] == "general_query"


def test_analyze_file_returns_percentage() -> None:
    response = client.post(
        "/analyze-file",
        files={"file": ("sample.txt", b"This is a sample text for analysis.", "text/plain")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "sample.txt"
    assert 0 <= payload["analysis"]["ai_generated_percentage"] <= 100
