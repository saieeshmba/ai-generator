from __future__ import annotations

import os

import httpx


class LLMService:
    def __init__(self) -> None:
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")

    async def generate_answer(self, prompt: str) -> str:
        question = (prompt or "").strip()
        if not question:
            return "Please provide a question."

        if self.provider == "openai" and self.openai_key:
            answer = await self._openai_chat(question)
            if answer:
                return answer

        if self.provider == "gemini" and self.gemini_key:
            answer = await self._gemini_chat(question)
            if answer:
                return answer

        return (
            "This is a local fallback answer because no AI API key is configured. "
            f"Your question was: {question}"
        )

    async def _openai_chat(self, prompt: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": "Be" + "arer " + self.openai_key}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
            body = response.json()
            return body["choices"][0]["message"]["content"].strip()
        except Exception:
            return ""

    async def _gemini_chat(self, prompt: str) -> str:
        model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            body = response.json()
            return body["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return ""
