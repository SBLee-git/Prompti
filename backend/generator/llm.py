from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    """직무 기술서 생성 시 사용할 LLM 모델 설정"""
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
