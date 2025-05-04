import json
import torch
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

#  KURE-v1 임베딩 모델 설정
embedding_model = HuggingFaceEmbeddings(
    model_name="nlpai-lab/KURE-v1",
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

#  ChromaDB 설정
db = Chroma(
    persist_directory="./db/interview_db",
    embedding_function=embedding_model,
    collection_name="interview_questions"
)

#  JSON 데이터 로드
with open("./data/interview_qa.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#  Document 객체 생성
documents = []
for item in data:
    content = f"Q: {item['question']}\nA: {item['answer']}"
    metadata = {
        "position_eng": item["tag_eng"],
        "position_kor": item["tag_kor"],
        "experience": item["experience"]
    }
    documents.append(Document(page_content=content.strip(), metadata=metadata))

#  Splitter 적용
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(documents)

#  ChromaDB에 저장
try:
    db.add_documents(chunks)
    print(f"✅ 총 {len(chunks)}개의 문서 청크가 저장되었습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")
