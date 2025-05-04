from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# ✅ 평가 프롬프트 정의
eval_prompt = PromptTemplate.from_template("""
당신은 AI 기반 면접 평가관입니다.

다음은 지원자의 면접 질문, 답변, 그리고 각 질문에 대한 모범답안입니다.
이 데이터를 기반으로 아래 항목에 따라 면접을 평가하세요:

1. ✅ **직무 이해도**: 질문에 대한 전반적인 이해도, 배경지식 반영 여부
2. ✅ **기술 활용 능력**: 기술 스택 언급, 실제 사용 경험, 구체적 기술 사례
3. ✅ **문제 해결 능력**: 문제 분석, 해결 과정의 논리성, 개선 제안 등
4. ✅ **종합 피드백**: 전반적인 강점/보완점, 추천 여부, 인상 깊은 부분

- 각 항목은 **짧고 명확하게 평가**하세요 (각 3~5줄)
- 마지막에 **질문/모범답안 목록**을 함께 정리해주세요
- 절대로 질문 외의 항목은 포함하지 마세요 (점수 X)

면접 기록:
{interview_data}

평가 결과:
""")

# ✅ 체인 반환 함수
def get_eval_chain():
    return eval_prompt | llm | StrOutputParser()
