import streamlit as st

def render(go):
    if "users" not in st.session_state:
        st.session_state.users = {}

    if "auth_user" not in st.session_state:
        st.session_state.auth_user = None

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "로그인"

    if "signup_success_message" not in st.session_state:
        st.session_state.signup_success_message = False

    st.title("🔐 로그인 / 회원가입")
    auth_mode = st.radio("모드 선택", ["로그인", "회원가입"], horizontal=True)
    st.session_state.auth_mode = auth_mode

    if auth_mode == "회원가입":
        st.subheader("📥 회원가입")
        email = st.text_input("이메일", key="signup_email").strip().lower()
        password = st.text_input("비밀번호", type="password", key="signup_pw")
        user_type = st.selectbox("사용자 유형", ["기업", "개인"], key="signup_type")

        # ✅ 회원가입 성공 메시지 유지
        if st.session_state.signup_success_message:
            st.success("✅ 회원가입 성공! 로그인 화면으로 이동해주세요.")
            st.session_state.signup_success_message = False

        if st.button("회원가입"):
            if email == "" or password == "":
                st.warning("이메일과 비밀번호를 모두 입력해주세요.")
            elif email in st.session_state.users:
                st.warning("이미 존재하는 계정입니다.")
            else:
                st.session_state.users[email] = {
                    "password": password,
                    "type": user_type
                }
                st.session_state.signup_success_message = True
                st.rerun()

    else:
        st.subheader("🔓 로그인")
        email = st.text_input("이메일", key="login_email").strip().lower()
        password = st.text_input("비밀번호", type="password", key="login_pw")
        user_type = st.selectbox("사용자 유형", ["기업", "개인"], key="login_type")

        if st.button("로그인"):
            users = st.session_state.users
            if (
                email in users and
                users[email]["password"] == password and
                users[email]["type"] == user_type
            ):
                st.session_state.auth_user = {
                    "email": email,
                    "type": user_type
                }
                st.success("🎉 로그인 성공!")
                go("generate" if user_type == "기업" else "interview_chat")
            else:
                st.error("❌ 이메일 / 비밀번호 / 사용자 유형이 일치하지 않습니다.")
