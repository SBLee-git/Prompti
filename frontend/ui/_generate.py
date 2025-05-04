import streamlit as st
import requests

def render(go):
    if "auth_user" not in st.session_state or st.session_state.auth_user.get("type") != "기업":
        st.error("기업 계정으로 로그인해야 합니다.")
        if st.button("로그인으로 돌아가기"):
            go("login")
        return

    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""
    if "questions_text" not in st.session_state:
        st.session_state.questions_text = ""

    user = st.session_state.auth_user
    st.sidebar.markdown("### 👤 로그인 정보")
    st.sidebar.write(f"**ID:** {user['email']}")
    st.sidebar.write(f"**유형:** {user['type']}")

    st.title("🏢 기업 전용 생성 페이지")
    st.subheader("📌 JD 생성 및 면접 질문 생성")

    position = st.selectbox("직무를 선택하세요", ["선택하세요", "데이터 엔지니어", "데이터 분석가", "머신러닝 엔지니어", "AI 엔지니어", "AI 연구원"])
    experience = st.selectbox("경력 수준을 선택하세요", ["신입", "3~5년", "5~10년", "10년 이상"])

    # ✅ JD 생성 요청 버튼만 먼저
    if st.button("📄 JD 생성 요청"):
        if position == "선택하세요":
            st.warning("직무를 선택해주세요.")
        else:
            with st.spinner("JD 생성 중..."):
                try:
                    response = requests.post("http://localhost:8000/generate/jd", json={"position": position, "experience": experience})
                    if response.status_code == 200:
                        st.session_state.jd_text = response.json()["jd"]
                        st.success("✅ JD 생성 완료!")
                    else:
                        st.error("JD 생성 실패")
                except Exception as e:
                    st.error(f"API 연결 오류: {e}")

    # ✅ JD 출력/수정/저장 + 그 아래 질문 생성 버튼
    if st.session_state.jd_text:
        st.subheader("📄 생성된 JD")
        st.session_state.jd_text = st.text_area("✍️ JD 수정 가능", value=st.session_state.jd_text, height=300)
        st.download_button(
            label="📥 JD 다운로드",
            data=st.session_state.jd_text,
            file_name=f"{position}_{experience}_JD.txt",
            mime="text/plain"
        )

        # ✅ JD 아래에 위치한 질문 생성 버튼
        if st.button("🧠 면접 질문 생성 요청"):
            with st.spinner("면접 질문 생성 중..."):
                try:
                    response = requests.post("http://localhost:8000/generate/interview", json={"position": position, "experience": experience})
                    if response.status_code == 200:
                        questions = response.json()["questions"]
                        cleaned_questions = [q.lstrip("0123456789. ").strip() for q in questions]
                        st.session_state.questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(cleaned_questions)])
                        st.success("✅ 질문 생성 완료!")
                    else:
                        st.error("면접 질문 생성 실패")
                except Exception as e:
                    st.error(f"API 연결 오류: {e}")

    # ✅ 질문 출력 (조건부)
    if st.session_state.questions_text:
        st.subheader("🧠 질문 리스트")
        st.session_state.questions_text = st.text_area("✍️ 질문 수정 가능", value=st.session_state.questions_text, height=300)

    if st.sidebar.button("🔓 로그아웃"):
        st.session_state.auth_user = None
        go("login")
