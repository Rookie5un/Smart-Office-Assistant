from typing import Dict, Any
from backend.app.services.llm_adapter import qwen_adapter

class TranslationService:
    @staticmethod
    def translate(text: str, target_lang: str = "中文") -> Dict[str, Any]:
        prompt = f"""
        请将以下文本翻译成 {target_lang}。保持专业办公语境，如果是会议内容，请确保术语准确。

        文本：
        {text}
        """

        messages = [
            {"role": "system", "content": "你是一个精通多国语言的同声传译专家。"},
            {"role": "user", "content": prompt}
        ]

        result = qwen_adapter.completion(messages)
        return {"translated_text": result}

translation_service = TranslationService()
