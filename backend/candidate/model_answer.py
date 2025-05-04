# backend/candidate/model_answer.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# ✅ 모범답안 생성 프롬프트
model_answer_prompt = PromptTemplate.from_template("""
당신은 모범답안을 작성하는 AI입니다.

다음 {position} 직무 ({experience}) 면접 질문에 대한 **모범적인 답변 예시**를 생성해주세요.
- 너무 길지 않게 (3~5문장)
- 포인트를 잘 짚은 실제적인 해당 직무와 경력에 맞는 실무자 답변처럼 보여야 합니다.
- 자신감 넘치고, 부드러운 어조를 사용해주세요.
- 답변은 구체적이고 전문적이어야 하며, 실제 경험이나 기술적 지식을 포함해야 합니다.

면접 질문:
{question}

모범답안:
""")

# ✅ 체인 반환 함수
def get_model_answer_chain():
    return model_answer_prompt | llm | StrOutputParser()
