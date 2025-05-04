# backend/candidate/feedback_chain.py
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

# ✅ 피드백 스키마 정의
class Feedback(BaseModel):
    직무_이해도: str = Field(..., alias="직무 이해도")
    기술_활용_능력: str = Field(..., alias="기술 활용 능력")
    문제_해결_능력: str = Field(..., alias="문제 해결 능력")
    전체_평가: str = Field(..., alias="전체 평가")

# ✅ 구조화 파서 준비
parser = PydanticOutputParser(pydantic_object=Feedback)

# ✅ JSON 예시 escape 처리
instructions = parser.get_format_instructions()
safe_instructions = instructions.replace("{", "{{").replace("}", "}}")

# ✅ GPT 프롬프트 구성
prompt = ChatPromptTemplate.from_template(f"""
당신은 AI 면접관입니다. 아래는 지원자의 면접 응답 이력입니다.  
각 항목을 평가하여 정성적 피드백을 작성하세요.

- '직무 이해도': 직무에 대한 기본 지식 및 관련 경험을 평가하세요.  
- '기술 활용 능력': 문제 해결 시 어떤 기술/도구를 활용했는지 평가하세요.  
- '문제 해결 능력': 주어진 질문에 대해 논리적 사고, 접근 방식 등을 평가하세요.  
- '전체 평가': 종합적으로 실무 적합성 및 강점/개선점을 요약하세요.

직무: {{position}}  
경력: {{experience}}  
면접 기록:
{{history}}

아래 JSON 형식으로만 출력하세요:  
{safe_instructions}
""")

def get_feedback_chain():
    return prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.5) | parser
