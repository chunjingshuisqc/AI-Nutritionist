import httpx
from typing import List, Dict, Optional, AsyncGenerator

from .config import settings


class LLMClient:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL.rstrip("/")
        self.model = settings.LLM_MODEL

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"]

    async def embed(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        url = (
            f"{settings.EMBEDDING_BASE_URL.rstrip('/')}"
            "/embeddings"
        )

        headers = {
            "Authorization": f"Bearer {settings.EMBEDDING_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.EMBEDDING_MODEL,
            "input": texts
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()

            return [
                item["embedding"]
                for item in response.json()["data"]
            ]


llm_client = LLMClient()