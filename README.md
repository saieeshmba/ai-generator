# ai-generator

Minimal AI generator API with:

- `/chat`: Ask any question and get an AI response.
- Intent detection for seminar-style queries.
- `/analyze-file`: Upload a text file and get estimated AI-generated percentage.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables (optional)

- `AI_PROVIDER` = `openai` or `gemini` (default: `openai`)
- `AI_MODEL` (default: `gpt-4o-mini`)
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GEMINI_MODEL` (default: `gemini-1.5-flash`)

If no API key is provided, `/chat` returns a local fallback answer.

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```