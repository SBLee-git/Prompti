from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple
from backend.generator.chain import get_jd_chain
from backend.generator.interview_final import get_interview_question_chain
from backend.candidate.followup_chain import get_followup_question_chain
from backend.candidate.feedback_chain import get_feedback_chain
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

# ✅ 요청 데이터 구조
class GenerateRequest(BaseModel):
    position: str
    experience: str

# ✅ JD 생성 API
@router.post("/jd")
def generate_jd(data: GenerateRequest):
    chain = get_jd_chain()
    jd = chain.invoke({
        "position": data.position,
        "experience": data.experience
    })
    return {"jd": jd}

# ✅ 면접 질문 생성 API
@router.post("/interview")
def generate_questions(data: GenerateRequest):
    chain = get_interview_question_chain(top_k=5)
    questions = chain(data.position, data.experience)
    return {"questions": questions.split("\n")}

# ✅ 꼬리질문 생성 요청 구조
class FollowupRequest(BaseModel):
    position: str
    experience: str
    question: str
    answer: str

# ✅ 꼬리 질문 생성 API
@router.post("/followup")
def generate_followup(data: FollowupRequest):
    chain = get_followup_question_chain()
    result = chain.invoke({
        "position": data.position,
        "experience": data.experience,
        "question": data.question,
        "answer": data.answer
    })

    print("[🔁 followup result]", result)  # 🔍 확인용

    if not result:
        result = "❗ 꼬리 질문을 생성하지 못했습니다. 다음 질문으로 넘어가주세요."

    return {"followup": result}

# ✅ 피드백 요청 구조
class FeedbackRequest(BaseModel):
    position: str
    experience: str
    history: List[Tuple[str, str, str, str]]  # 질문, 답변, 꼬리질문, 답변2

# ✅ 피드백 생성 API
@router.post("/feedback")
def generate_feedback(data: FeedbackRequest):
    chain = get_feedback_chain()

    # 면접 히스토리 문자열로 합치기
    history_str = "\n".join([
        f"[질문]: {q}\n[답변]: {a}\n[꼬리질문]: {fq}\n[꼬리답변]: {fa}"
        for q, a, fq, fa in data.history
    ])

    # GPT 호출 및 구조화된 결과 받기
    feedback_obj = chain.invoke({
        "position": data.position,
        "experience": data.experience,
        "history": history_str
    })

    print(feedback_obj)  # 🔍 확인용
    
    # Pydantic 객체 → dict로 변환하여 반환
    return feedback_obj.dict(by_alias=True)
