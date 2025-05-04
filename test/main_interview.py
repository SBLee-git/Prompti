from backend.generator.interview_final import get_interview_question_chain

if __name__ == "__main__":
    chain = get_interview_question_chain(top_k=5)
    result = chain("데이터 엔지니어", "신입",debug=True)

    print("📄 최종 면접 질문 리스트:")
    print(result)