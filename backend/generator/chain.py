from backend.generator.prompt import get_jd_prompt
from backend.generator.retriever import get_jd_retriever
from backend.generator.llm import get_llm
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from dotenv import load_dotenv
load_dotenv()

def get_jd_chain():
    """직무 기술서 자동 생성 Chain"""
    retriever = get_jd_retriever()
    prompt = get_jd_prompt()
    llm = get_llm()

    # LangChain 체인 구성 (RAG 스타일)
    chain = (
        {
            "context": itemgetter("position") | retriever,
            "position": itemgetter("position"),
            "experience": itemgetter("experience")
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

    
