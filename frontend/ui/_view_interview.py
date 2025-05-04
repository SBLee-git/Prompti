# ✅ _view_interview.py — render(go) 포함 최종 완성본
import streamlit as st
from backend.storage.interview_store import load_interview_list, load_interview_file

def render(go):
    if "auth_user" not in st.session_state or st.session_state.auth_user.get("type") != "개인":
        st.error("개인 계정으로 로그인해야 합니다.")
        if st.button("로그인으로 이동"):
            go("login")
        return

    user = st.session_state.auth_user
    st.title("📁 면접 기록 조회")
    st.sidebar.markdown("### 👤 로그인 정보")
    st.sidebar.write(f"**ID:** {user['email']}")
    st.sidebar.write(f"**유형:** {user['type']}")

    file_list = load_interview_list(user_email=user["email"])
    if not file_list:
        st.info("저장된 면접 기록이 없습니다.")
        return

    selected_file = st.selectbox("📂 조회할 면접 기록을 선택하세요:", file_list)
    if selected_file:
        data = load_interview_file(selected_file)
        st.subheader(f"📌 직무: {data['position']} ({data['experience']})")
        st.caption(f"🕒 날짜: {data['timestamp']}")

        st.markdown("### 💬 면접 대화 내용")
        for i, (q, a, fq, fa) in enumerate(data["history"]):
            st.markdown(f"**{i+1}. 질문:** {q}")
            st.markdown(f"🙋‍♂️ 답변: {a}")
            st.markdown(f"🔄 꼬리 질문: {fq}")
            st.markdown(f"🙋‍♂️ 답변2: {fa}")
            st.divider()

        st.markdown("### 📊 피드백 결과")
        feedback = data["feedback"]
        st.markdown(f"**직무 이해도:** {feedback['understanding']}")
        st.markdown(f"**기술 활용 능력:** {feedback['skills']}")
        st.markdown(f"**문제 해결 능력:** {feedback['problem_solving']}")
        st.markdown(f"**전체 평가:** {feedback['overall']}")

        st.markdown("### 📘 모범 답안")
        for i, item in enumerate(feedback["samples"]):
            st.markdown(f"**{i+1}. 질문:** {item['question']}")
            st.markdown(f"💡 모범답안: {item['answer']}")
            st.divider()

    if st.sidebar.button("🔓 로그아웃"):
        st.session_state.auth_user = None
        go("login")