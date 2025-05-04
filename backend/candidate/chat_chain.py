# backend/candidate/chat_chain.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.generator.retriever import get_jd_retriever  # ✅ JD 검색기 재활용

# ✅ LLM 설정
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    max_tokens=512
)

# ✅ 1. 메인 질문 프롬프트 (JD context 포함)
main_question_prompt = PromptTemplate.from_template("""
당신은 AI 기반 면접관입니다.

아래 포지션명, 경력 수준, 그리고 관련 직무 설명(context)을 참고하여
**면접 질문 1개만 생성**하세요.

- 반드시 **질문만 출력**하세요 (번호/설명 없이)
- 면접 질문은 포지션명/경력에 맞는 실무적인 질문이 되도록 하세요

포지션명: {position}
경력 수준: {experience}

직무 설명(context):
{context}

면접 질문:
""")

# ✅ 2. 꼬리 질문 프롬프트 (이전 답변 기반)
followup_question_prompt = PromptTemplate.from_template("""
당신은 AI 기반 면접관입니다.

이전 면접 질문과 지원자의 답변을 참고하여, **꼬리 질문(심화 질문)**을 1개 생성하세요.
- 반드시 **질문만 출력**하세요 (번호/설명 없이)
- 심화 질문은 지원자의 답변 내용을 바탕으로 더욱 깊이 있는 내용을 유도하세요
- 이전에 생성한 질문과 유사한 질문은 피해주세요.

이전 질문: {prev_question}
지원자 답변: {answer}

꼬리 질문:
""")

# ✅ JD 기반 RAG 질문 체인
def get_main_question_chain_rag():
    retriever = get_jd_retriever()

    def generate_question(inputs: dict) -> str:
        query = f"{inputs['position']} {inputs['experience']}"
        docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt_input = {
            "position": inputs["position"],
            "experience": inputs["experience"],
            "context": context
        }

        chain = main_question_prompt | llm | StrOutputParser()
        return chain.invoke(prompt_input)

    return generate_question

# ✅ 꼬리질문 체인 (GPT 단독)
def get_followup_question_chain():
    return followup_question_prompt | llm | StrOutputParser()
