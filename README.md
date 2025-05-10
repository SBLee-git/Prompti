# 🧠 서비스 소개: **프롬프티 (PromptI)**

> AI 기반 채용 보조 서비스
> 
> 
> 채용 담당자와 구직자 모두를 위한 직무 기술서 생성 + AI 대화형 면접 시뮬레이션
> 

---

## ✅ 서비스 개요

프롬프티(PromptI)는 다음 기능을 제공합니다:

- **직무 기술서 자동 생성**
- **AI 면접 질문 생성 및 시뮬레이션**
- **면접 피드백 및 기록 저장**

수집된 데이터는 Chroma DB를 기반으로 벡터 검색 및 질문 생성을 수행합니다.

---
## ✅ 나의 역할

- **FastAPI/Streamlit 기반 프론트엔드 및 백엔드 통합 개발**

- **RAG 기반 AI 시스템의 구조 설계 및 체인 구성**

- **기업/개인 사용자 분리 설계 및 인터페이스 설계**

- **면접 질문 생성 로직 및 피드백 평가 로직 설계 및 최적화**

## 📊 데이터 수집 및 저장

| 항목 | 수집 방식 | 활용 용도 |
| --- | --- | --- |
| **직무 기술서** | 웹 크롤링 | 최신 직무 정보 기반 생성 |
| **면접 질문** | OpenAI API 활용 | 다양한 직무에 맞춘 질문 생성 |
- 데이터는 전처리 후 **Chroma DB**에 저장됩니다.

---

## 👤 사용자 유형 및 초기 화면

- **초기 진입 화면**: 로그인 화면
- **회원가입 시 입력**: 이메일 / 비밀번호 / 회원 유형(개인 or 기업)
- **로그인 시** 회원 유형에 따라 맞춤 기능 제공

---

## 🧑‍💼 기업 사용자 기능

### 1. 직무 기술서 생성

- 채용 포지션 & 경력 입력
- 관련 데이터 벡터 검색
- 자동 생성된 JD를 **수정/저장/복사** 가능

### 2. 면접 질문 생성

- 포지션 & 경력 기반
- 관련 질문을 벡터 DB에서 검색해 자동 제공

---

## 🙋 개인 사용자 기능

### 1. AI 대화형 면접 챗봇

- 포지션/경력 선택 → 질문 리스트 생성
- 실시간 대화형 면접
- 답변에 따라 **꼬리 질문 자동 생성**

### 2. 면접 피드백 생성

- 평가 항목:
    - 직무 이해도
    - 기술 활용 능력
    - 문제 해결 능력
    - 전체 평가
- **모범 답변**도 자동 제공

### 3. 면접 기록 확인

- 대화 기록 / 피드백 / 모범 답변이 **로컬 서버에 저장**
- 이전 면접 내역을 기록 확인 화면에서 열람 가능

### 4. 서비스 화면
![Company1](https://github.com/user-attachments/assets/4a024206-f23e-4ee8-8c7b-b7334f9bbb1b)
![Company2](https://github.com/user-attachments/assets/19495373-dd01-4c26-87f3-14777095d7c3)
![Company3](https://github.com/user-attachments/assets/b963142f-3a15-4b17-9982-a0cca94baf59)
![Personal1](https://github.com/user-attachments/assets/dbdf34e9-a401-4da8-99bc-f66e856775c1)
![Personal2-1](https://github.com/user-attachments/assets/2c49e523-dc5d-45c6-881a-22799be5440d)
![Personal2-2](https://github.com/user-attachments/assets/27bb801a-b163-48c0-b39d-b2cf3dd6fcb0)
![Personal3-1](https://github.com/user-attachments/assets/a10ab54c-1253-4c96-b668-2d6c4f9655ab)
![Personal3-2](https://github.com/user-attachments/assets/2f22776d-1a69-49c9-8ba3-103bbf046025)
![Personal4](https://github.com/user-attachments/assets/a56adbfe-998f-40c9-b5e3-584306a5d3dd)

---

## 🌟 사용자 가치

- **채용 담당자**: 반복 업무 자동화, 빠른 JD 작성
- **구직자**: 실전형 AI 면접, 피드백 기반 자기개발
- 대화 기록과 피드백까지 저장되어 **지속적인 개선 가능**
