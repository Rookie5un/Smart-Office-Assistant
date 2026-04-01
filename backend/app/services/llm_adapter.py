from typing import Optional, List, Dict, Any
from openai import OpenAI
from backend.app.core.config import settings

class LLMAdapter:
    def __init__(self, provider: str = "qwen"): # qwen or doubao
        self.provider = provider
        if provider == "qwen":
            self.client = OpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL
            )
            self.model = "qwen-plus" # Default model for Qwen
        elif provider == "doubao":
            self.client = OpenAI(
                api_key=settings.DOUBAO_API_KEY,
                base_url=settings.DOUBAO_BASE_URL
            )
            # NOTE: Doubao usually requires endpoint ID as model name
            self.model = "ep-xxxxxx-xxxx"

    def completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

# Helper instances
qwen_adapter = LLMAdapter(provider="qwen")
doubao_adapter = LLMAdapter(provider="doubao")
