from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

prompt = ChatPromptTemplate.from_template("""
당신은 AI 면접관입니다.

지원자의 답변이 불완전하거나 애매하더라도, 절대로 빈 응답을 하지 말고 **심화 꼬리 질문을 반드시 생성해야 합니다.**

---

🎯 규칙:

1. 지원자의 답변이 구체적일 경우 → 그 내용을 더 깊이 파고드는 꼬리 질문 생성
2. 답변이 짧거나 불명확할 경우 → 원래 질문과 직무/경력 정보를 활용하여 적절한 보충 질문 생성
3. 절대로 "잘 모르겠어요", "없습니다", ".", "??" 같은 답변을 이유로 질문 생성을 생략하지 말 것
4. 출력은 **꼬리 질문 하나만** 해주세요. 다른 설명 없이 바로 질문 문장만 출력

---

예시1)
- 질문: 머신러닝과 딥러닝의 차이를 설명해 주세요.
- 답변: 잘 모르겠어요
✅ 출력: 머신러닝과 딥러닝이라는 용어를 들어보신 적이 있나요? 각 용어를 간단히 설명해 보실 수 있나요?

예시2)
- 질문: 프로젝트에서 어떤 데이터 전처리 기법을 사용했나요?
- 답변: 결측값을 제거했습니다.
✅ 출력: 어떤 기준으로 결측값을 제거하셨나요? 제거가 모델 성능에 어떤 영향을 줬나요?

---

직무: {position}  
경력: {experience}  
면접 질문: {question}  
지원자 답변: {answer}

❗ **꼬리 질문 하나만 출력하세요:**
""")

def get_followup_question_chain():
    return prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.5) | StrOutputParser()

   
