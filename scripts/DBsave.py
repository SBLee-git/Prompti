import pandas as pd
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import torch 
from dotenv import load_dotenv
load_dotenv()

# KURE-v1 임베딩 모델로 변경
embedding = HuggingFaceEmbeddings(
    model_name="nlpai-lab/KURE-v1",
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

#  CSV 파일 로드
file_path = "./data/job_list_cleaned.csv"   
df = pd.read_csv(file_path)

#  텍스트 데이터 전처리
def create_job_description(row):
    return f"""
    포지션명: {row['포지션명']}
    경력: {row['경력']}
    
    주요업무:
    {row['주요업무']}
    
    자격요건:
    {row['자격요건']}  
    
    우대사항:
    {row['우대사항']}
    """.strip()

job_descriptions = df.apply(create_job_description, axis=1).tolist()

#  Document 객체 변환
documents = [
    Document(
        page_content=job_text,
        metadata={"position": row['포지션명'], "experience": row['경력']}
    )
    for job_text, (_, row) in zip(job_descriptions, df.iterrows())
]

#  Splitter 적용
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)

#  ChromaDB에 저장
db = Chroma.from_documents(
    chunks,
    embedding=embedding,
    persist_directory="./db/chroma_db",
    collection_name="job_descriptions"
)


print(f" ChromaDB에 직무 기술서 데이터 저장 완료! (총 {len(chunks)}개 청크 저장)")
