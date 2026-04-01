from typing import Dict, Any, List
from backend.app.services.llm_adapter import qwen_adapter

class MeetingService:
    @staticmethod
    def generate_summary(transcript: str) -> Dict[str, Any]:
        prompt = f"""
        请根据以下会议记录，提取会议摘要、待办事项(Action Items)和关键决策点。
        要求格式清晰，使用 Markdown 格式输出。

        会议记录：
        {transcript}
        """

        messages = [
            {"role": "system", "content": "你是一个专业的会议速记员和行政助理，擅长提炼核心信息。"},
            {"role": "user", "content": prompt}
        ]

        result = qwen_adapter.completion(messages)
        return {"summary": result}

meeting_service = MeetingService()
