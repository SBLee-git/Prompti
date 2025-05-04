import streamlit as st
import requests

def render(go):
    if "auth_user" not in st.session_state or st.session_state.auth_user.get("type") != "개인":
        st.error("개인 계정으로 로그인해야 합니다.")
        if st.button("로그인으로 이동"):
            go("login")
        return

    user = st.session_state.auth_user
    st.sidebar.markdown("### 👤 로그인 정보")
    st.sidebar.write(f"**ID:** {user['email']}")
    st.sidebar.write(f"**유형:** {user['type']}")

    # ✅ 상태 초기화
    for key, default in [
        ("step", 0),
        ("history", []),
        ("chat_log", []),
        ("waiting_followup", False),
        ("feedback", None),
        ("current_round", 0),
        ("latest_answer", ""),
        ("current_followup", ""),
        ("position", None),
        ("experience", None),
        ("current_question", None)
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    st.title("🧑‍💼 AI 가상 면접 시뮬레이션")

    # ✅ 면접 시작 전
    if st.session_state.step == 0:
        st.subheader("🎯 면접을 시작합니다")
        position_options = ["선택하세요", "데이터 분석가", "데이터 엔지니어", "머신러닝 엔지니어", "AI 엔지니어", "AI 연구원"]
        experience_options = ["신입", "3~5년", "5~10년", "10년 이상"]
        selected_position = st.selectbox("직무를 선택하세요", position_options)
        selected_experience = st.selectbox("경력을 선택하세요", experience_options)

        if st.button("면접 시작하기") and selected_position != "선택하세요":
            st.session_state.position = selected_position
            st.session_state.experience = selected_experience
            st.session_state.step = 1
            st.session_state.chat_log = []
            st.session_state.history = []
            st.session_state.feedback = None
            st.session_state.current_round = 0
            st.session_state.waiting_followup = False

            try:
                response = requests.post("http://localhost:8000/generate/interview", json={
                    "position": selected_position,
                    "experience": selected_experience
                })
                result = response.json()
                question = result["questions"][0]
                st.session_state.current_question = question
                st.session_state.chat_log.append({"role": "system", "content": question})
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"❌ 첫 질문 생성 실패: {e}")
                return

    else:
        # ✅ 채팅 로그 출력
        for msg in st.session_state.chat_log:
            if msg["role"] == "system":
                st.markdown(f"""
                <div style='max-width: 65%; display:inline-block; background-color: #4b4b4b; color: white; padding: 12px 16px; border-radius: 18px 18px 18px 6px; margin-bottom: 12px;'>
                    💬 <b>질문:</b> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='max-width: 65%; display:inline-block; background-color: #1e90ff; color: white; padding: 12px 16px; border-radius: 18px 18px 6px 18px; margin-left: auto; float: right; text-align: right; margin-bottom: 12px;'>
                    🙋‍♂️ <b>답변:</b> {msg['content']}
                </div><div style='clear: both;'></div>
                """, unsafe_allow_html=True)

        # ✅ 사용자 입력 or 피드백 버튼
        if st.session_state.current_round >= 3 and st.session_state.step != 100:
            st.warning("면접이 완료되었습니다. 아래 버튼을 눌러 피드백을 확인하세요.")
            if st.button("📝 피드백 생성하기"):
                try:
                    res = requests.post("http://localhost:8000/generate/feedback", json={
                        "position": st.session_state.position,
                        "experience": st.session_state.experience,
                        "history": st.session_state.history
                    })
                    st.session_state.feedback = res.json()
                    st.session_state.step = 100
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 피드백 생성 실패: {e}")
            return  # 입력창 숨기기

        else:
            user_input = st.chat_input("답변을 입력하세요")
            if user_input:
                st.session_state.chat_log.append({"role": "user", "content": user_input})

                if st.session_state.step % 2 == 0:
                    # 기본 질문 답변 → 꼬리질문 생성 준비
                    st.session_state.latest_answer = user_input
                    st.session_state.waiting_followup = True
                    st.session_state.step += 1
                    st.rerun()
                else:
                    # 꼬리 질문 답변 → history 저장 + 다음 질문
                    st.session_state.history.append((
                        st.session_state.current_question,
                        st.session_state.latest_answer,
                        st.session_state.current_followup,
                        user_input
                    ))
                    st.session_state.current_round += 1
                    st.session_state.step += 1

                    if st.session_state.current_round < 3:
                        try:
                            response = requests.post("http://localhost:8000/generate/interview", json={
                                "position": st.session_state.position,
                                "experience": st.session_state.experience
                            })
                            result = response.json()
                            next_q = result["questions"][st.session_state.current_round]
                            st.session_state.current_question = next_q
                            st.session_state.chat_log.append({"role": "system", "content": next_q})
                        except Exception as e:
                            st.error(f"❌ 다음 질문 생성 실패: {e}")
                    st.rerun()

        # ✅ 꼬리 질문 생성 처리
        if st.session_state.waiting_followup:
            try:
                response = requests.post("http://localhost:8000/generate/followup", json={
                    "position": st.session_state.position,
                    "experience": st.session_state.experience,
                    "question": st.session_state.current_question,
                    "answer": st.session_state.latest_answer
                })
                followup = response.json().get("followup")

                if not followup:
                    followup = "⚠️ 꼬리 질문을 생성하지 못했습니다. 대신 이 주제에 대해 궁금한 점이 있으신가요?"

                st.session_state.current_followup = followup
                st.session_state.chat_log.append({"role": "system", "content": followup})
                st.session_state.waiting_followup = False
                st.rerun()
            except Exception as e:
                st.error(f"❌ 꼬리 질문 생성 실패: {e}")

    # ✅ 피드백 출력
    if st.session_state.step == 100 and st.session_state.feedback:
        st.subheader("📊 종합 피드백")
        fb = st.session_state.feedback
        st.markdown(f"""
        - **직무 이해도**: {fb.get("직무 이해도", "없음")}
        - **기술 활용 능력**: {fb.get("기술 활용 능력", "없음")}
        - **문제 해결 능력**: {fb.get("문제 해결 능력", "없음")}
        - **전체 평가**: {fb.get("전체 평가", "없음")}
        """)

        if st.button("🔄 면접 다시 시작하기"):
            for k in ["step", "history", "chat_log", "waiting_followup", "feedback", "current_round", "latest_answer", "current_followup"]:
                st.session_state.pop(k, None)
            st.rerun()
