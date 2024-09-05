import os
from abc import ABC, abstractmethod
from typing import Dict, Any
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
import re
from unified_logging import backend_logger as logger

load_dotenv()

class LLMConfig(BaseModel):
    api_key: str = Field(..., env='OPENROUTER_API_KEY')
    api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    model: str = "openai/gpt-4o-mini-2024-07-18"

class LLMBase(ABC):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.logger = logger

    async def call_llm(self, messages: list) -> str:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.config.model,
            "messages": messages
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.config.api_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    @abstractmethod
    async def generate(self, input_data: Dict[str, Any]) -> str:
        pass

    def format_llm_response(self, response: str) -> dict:
        # ... (保持原有的 format_llm_response 方法实现)
        pass
