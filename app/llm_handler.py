# app/llm_handler.py

from app.llm_utils import ask_llm

def handle_llm_query(question: str, schema: dict):
    try:
        return ask_llm(question, schema)
    except Exception as e:
        return f"❌ LLM Handler Error: {str(e)}"
