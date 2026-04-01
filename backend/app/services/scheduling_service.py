from typing import Dict, Any
from backend.app.services.llm_adapter import qwen_adapter
import datetime

class SchedulingService:
    @staticmethod
    def parse_intent(text: str) -> Dict[str, Any]:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = f"""
        当前时间是：{current_time}
        请解析以下自然语言描述的会议预约意图，提取出以下信息（如果存在）：
        1. 主题 (subject)
        2. 开始时间 (start_time, 格式：YYYY-MM-DD HH:MM)
        3. 参与人员 (participants, 列表)
        4. 持续时间 (duration_minutes)

        意图描述：
        {text}

        请以 JSON 格式输出结果。
        """

        messages = [
            {"role": "system", "content": "你是一个高效的日程管理助手，擅长从自然语言中提取结构化的日程信息。"},
            {"role": "user", "content": prompt}
        ]

        result = qwen_adapter.completion(messages, response_format={ "type": "json_object" })
        return {"schedule": result}

scheduling_service = SchedulingService()
