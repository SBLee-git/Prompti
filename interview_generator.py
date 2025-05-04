# interview_generator.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# GPT 모델 설정
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

question_prompt = PromptTemplate.from_template("""
당신은 {position} 직무의 전문가입니다.
경력 {experience} 수준의 지원자에게 적절한 면접 질문 5개와 각 질문에 대한 모범 답안을 생성해 주세요.

❗ 각 질문은 해당 경력 수준에서 꼭 물어볼만한 난이도로 작성되어야 합니다.

예시:
- 신입~2년: 개념 설명, 기초 활용, 기본 실무 질문
- 3~5년: 실무 적용, 간단한 설계, 업무 도구 경험
- 5~10년 이상: 아키텍처 구성, 최적화 전략, 실무 개선 제안

형식:
1. 질문 내용
모범답안 내용
""")

def generate_questions(position: str, experience: str) -> str:
    """GPT를 활용하여 면접 질문 및 모범답안을 생성하는 함수"""
    prompt = question_prompt.format(position=position, experience=experience)
    return llm.invoke(prompt)
