import torch
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_qa_retriever(db_path="./db/interview_db"):
    embedding = HuggingFaceEmbeddings(
        model_name="nlpai-lab/KURE-v1",
        model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding,
        collection_name="interview_questions"
    )

    retriever = db.as_retriever(search_kwargs={"k": 5})
    return retriever
