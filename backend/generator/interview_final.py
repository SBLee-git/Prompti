import re, time
from functools import lru_cache
import torch
from diskcache import Cache
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from operator import itemgetter

from backend.generator.interview_prompt import get_interview_prompt
from backend.generator.skill_extract import extract_skills
from backend.generator.interview_retriever import get_qa_retriever
from dotenv import load_dotenv
load_dotenv()

def get_interview_question_chain(top_k: int = 5):
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        max_tokens=512
    )
    prompt = get_interview_prompt()
    retriever = get_qa_retriever()

    @lru_cache(maxsize=100)
    def get_skills(position: str, experience: str):
        return extract_skills(position, experience)

    def extract_valid_questions(raw_output: str) -> list[str]:
        lines = raw_output.split("\n")
        return [
            line.strip()
            for line in lines
            if re.match(r"^\s*\d{1,2}\.\s+.+", line.strip())
        ]

    def chain_executor(position: str, experience: str, debug: bool = False):
        start_time = time.time()
        
        # 1. 기술 키워드 추출
        skills = get_skills(position, experience)
        skill_text = "\n".join(skills)

        # 2. 검색 (RAG)
        query = f"{position} {experience}"
        docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)

        # 3. GPT 입력 구성
        prompt_input = {
            "position": position,
            "experience": experience,
            "skills": skill_text,
            "context": context
        }

        # 4. 질문 생성 
        chain = prompt | llm | StrOutputParser()
        raw_output = chain.invoke(prompt_input)
        questions = extract_valid_questions(raw_output)

        if debug:
            print("🧠 기술 키워드:\n", skill_text)
            print("\n📚 검색된 문서(context):")
            for i, doc in enumerate(docs, 1):
                print(f"\n[{i}] {doc.page_content}\n---")
            print(f"\n⏱️ 생성 시간: {round(time.time() - start_time, 2)}초")

        return "\n".join(questions[:10])  # 혹시 10개 미만이면 있는 것까지만 반환

    return chain_executor


