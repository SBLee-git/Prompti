import torch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from backend.generator.interview_retriever import get_qa_retriever

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 기술 키워드 추출용 프롬프트
skill_prompt = PromptTemplate.from_template("""
아래는 특정 직무 및 경력 수준에 대한 설명입니다.
이 직무를 수행하는 데 필요한 기술 요소(프로그래밍 언어, 라이브러리, 프레임워크, 도구 등)를
줄바꿈 형태의 목록으로 정리해주세요.

직무 설명:
{text}

경력 수준: {experience}

기술 요소 목록:
""")

def extract_skills(position: str, experience: str) -> list:
    retriever = get_qa_retriever()
    query = f"{position} {experience}"

    docs = retriever.invoke(query)
    if not docs:
        return []

    job_text = "\n\n".join(doc.page_content for doc in docs)
    prompt = skill_prompt.format(text=job_text, experience=experience)
    response = llm.invoke(prompt).content

    return [line.strip("-•● ").strip() for line in response.strip().split("\n") if line.strip()]


# ✅ 테스트 실행 (선택)
# if __name__ == "__main__":
#     test_position = "AI 엔지니어"
#     test_experience = "신입"
#     skills = extract_skills(test_position, test_experience)
#     print(f"\n📌 [{test_position} / {test_experience}] 기술 키워드 추출 결과:")
#     for i, skill in enumerate(skills, 1):
#         print(f"{i}. {skill}")
