from __future__ import annotations

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field

from app.services.ai_detector import estimate_ai_percentage
from app.services.intent import detect_intent
from app.services.llm import LLMService

app = FastAPI(title="AI Generator API", version="1.0.0")
llm_service = LLMService()


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    intent: str
    answer: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    intent = detect_intent(request.question)
    answer = await llm_service.generate_answer(request.question)
    return ChatResponse(intent=intent, answer=answer)


@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)) -> dict:
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    analysis = estimate_ai_percentage(text)
    return {
        "filename": file.filename,
        "analysis": analysis,
    }
