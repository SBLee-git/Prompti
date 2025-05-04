# backend/candidate/interview_session.py

"""
전체 면접 흐름을 제어하는 컨트롤러 모듈
질문1 → 답변1 → 꼬리질문1 → 답변1 → ... 3세트 반복
"""

from backend.candidate.chat_chain import get_main_question_chain, get_followup_question_chain

class InterviewSession:
    def __init__(self, position: str, experience: str):
        self.position = position
        self.experience = experience

        self.main_chain = get_main_question_chain()
        self.followup_chain = get_followup_question_chain()

        self.history = []  # 전체 질문/답변 히스토리 저장
        self.step = 0      # 현재 질문 번호 (0~5)

    def is_finished(self) -> bool:
        return self.step >= 6  # 질문3 + 꼬리질문3 = 6개

    def next_question(self, answer: str = None) -> str:
        """
        사용자의 답변을 받고 다음 질문을 생성
        step 기준으로 질문 종류 결정
        """
        # 사용자 답변 저장 (이전 질문의)
        if self.step > 0 and answer:
            self.history[-1]["answer"] = answer

        # 종료 조건
        if self.is_finished():
            return None

        # 메인 질문 (0, 2, 4)
        if self.step % 2 == 0:
            question = self.main_chain.invoke({
                "position": self.position,
                "experience": self.experience
            })
        # 꼬리 질문 (1, 3, 5)
        else:
            prev_qa = self.history[-1]
            question = self.followup_chain.invoke({
                "prev_question": prev_qa["question"],
                "answer": prev_qa["answer"]
            })

        # 질문 저장
        self.history.append({
            "step": self.step,
            "question": question,
            "answer": None
        })
        self.step += 1
        return question

    def get_result(self) -> list[dict]:
        return self.history
