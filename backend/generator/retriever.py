import torch
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_jd_retriever(db_path="./db/chroma_db"):
    embedding = HuggingFaceEmbeddings(
        model_name="nlpai-lab/KURE-v1",
        model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding,
        collection_name="job_descriptions"
    )

    retriever = db.as_retriever(search_kwargs={"k": 5})
    return retriever


# # ✅ 실행 예시 (테스트용)
# if __name__ == "__main__":
#     position = "AI 엔지니어"
#     experience = "5년 이상"
#     retriever = get_jd_retriever()
#     query = f"Position: {position}, Experience: {experience}"
#     results = retriever.invoke(query)

#     for i, doc in enumerate(results, 1):
#         print(f"\n🔹 [{i}] 포지션: {doc.metadata['position']} / 경력: {doc.metadata['experience']}")
#         print(f"📄 내용: {doc.page_content[:300]}...\n---")
