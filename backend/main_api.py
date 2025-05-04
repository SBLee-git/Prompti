# backend/main.py

from fastapi import FastAPI
from backend.api.api import router as generate_router

app = FastAPI()

# API 라우터 등록
app.include_router(generate_router, prefix="/generate", tags=["Generate"])

@app.get("/")
def read_root():
    return {"message": "🔥 FastAPI 서버 실행 중입니다."}
