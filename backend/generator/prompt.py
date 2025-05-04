from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

def get_jd_prompt():
    """직무 기술서 자동 생성 프롬프트"""
    return PromptTemplate.from_template(
        """
        당신은 HR 담당자를 돕는 AI입니다.  
        주어진 포지션명과 경력 수준을 참고하여 직무 기술서를 생성하세요.
        If you don't know the answer, just say that you don't know.  
        아래는 검색된 관련 직무 기술서입니다.  
        이를 바탕으로 완전한 직무 기술서를 작성해주세요.

        - 포지션명: {position}
        - 경력: {experience}

        검색된 직무 기술서:
        {context}

        최종 직무 기술서를 아래 항목만 포함하여 작성하세요:
        - 주요업무
        - 자격요건
        - 우대사항

        ❗ 다음 항목은 작성하지 마세요:
        - "직무 기술서:"라는 제목
        - 포지션명, 경력 항목 반복 출력
        - "기타" 섹션
        """
        
    )
