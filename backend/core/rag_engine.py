import json
from typing import Dict, List, Optional

from .llm_client import llm_client
from .vector_store import vector_store


class RAGEngine:
    def __init__(self):
        self.system_prompt = """你是一位专业的AI营养师，具备临床营养学知识。
你的职责是根据用户体检报告、身体信息和口味偏好提供饮食建议。

请遵循以下原则：
1. 建议应具有营养学依据
2. 针对异常体检指标给出饮食调整建议
3. 避免用户过敏或不喜欢的食物
4. 食谱应适合家庭烹饪
5. 严重异常指标应建议用户就医
6. 仅提供饮食辅助建议，不替代医生诊断
"""

    async def retrieve(
        self,
        query: str,
        filter_dict: Optional[Dict] = None,
        top_k: int = 5
    ) -> List[Dict]:
        return await vector_store.search(
            query,
            top_k=top_k,
            filter_dict=filter_dict
        )

    def build_context(self, docs: List[Dict]) -> str:
        if not docs:
            return "暂无匹配知识，请基于通用营养原则回答。"

        context_parts = ["以下是相关营养知识："]

        for index, doc in enumerate(docs, 1):
            context_parts.append(
                f"【知识{index}】\n{doc['content']}"
            )

        return "\n\n".join(context_parts)

    def _build_prompt(
        self,
        health_data: Dict,
        taste_preferences: Dict,
        user_info: Dict,
        health_issues: List[str],
        context: str
    ) -> str:
        return f"""
请为用户生成一份7天周食谱。

用户基本信息：
{json.dumps(user_info, ensure_ascii=False, indent=2)}

体检信息：
{json.dumps(health_data, ensure_ascii=False, indent=2)}

识别出的健康问题：
{json.dumps(health_issues, ensure_ascii=False)}

口味与饮食偏好：
{json.dumps(taste_preferences, ensure_ascii=False, indent=2)}

营养知识参考：
{context}

请严格返回JSON，不要添加Markdown代码块，格式如下：
{{
  "title": "食谱标题",
  "health_summary": {{
    "main_issues": [],
    "bmi_advice": ""
  }},
  "nutrition_goals": [],
  "days": [
    {{
      "day": "周一",
      "breakfast": "",
      "lunch": "",
      "dinner": ""
    }}
  ],
  "shopping_list": []
}}
"""

    async def generate_meal_plan(
        self,
        health_data: Dict,
        taste_preferences: Dict,
        user_info: Dict
    ) -> str:
        health_issues = []

        if (health_data.get("fasting_glucose") or 0) > 6.1:
            health_issues.append("高血糖")

        if (health_data.get("total_cholesterol") or 0) > 5.2:
            health_issues.append("高胆固醇")

        if (health_data.get("triglycerides") or 0) > 1.7:
            health_issues.append("高甘油三酯")

        if (health_data.get("systolic_bp") or 0) >= 140:
            health_issues.append("高血压")

        if (health_data.get("uric_acid") or 0) > 420:
            health_issues.append("高尿酸")

        query = " ".join(
            ["营养食谱设计"] + health_issues
        )

        docs = await self.retrieve(query, top_k=8)
        context = self.build_context(docs)

        prompt = self._build_prompt(
            health_data,
            taste_preferences,
            user_info,
            health_issues,
            context
        )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return await llm_client.chat(
            messages,
            temperature=0.8,
            max_tokens=8192
        )

    async def chat(
        self,
        message: str,
        context_data: Optional[Dict] = None
    ) -> str:
        docs = await self.retrieve(message, top_k=5)
        context = self.build_context(docs)

        extra_context = ""
        if context_data:
            extra_context = json.dumps(
                context_data,
                ensure_ascii=False
            )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": (
                    f"用户咨询：{message}\n\n"
                    f"用户上下文：{extra_context}\n\n"
                    f"相关知识：{context}"
                )
            }
        ]

        return await llm_client.chat(
            messages,
            temperature=0.7,
            max_tokens=2048
        )


rag_engine = RAGEngine()