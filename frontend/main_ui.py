# ✅ main_ui.py — 완전 최적화 + generate 포함
import streamlit as st
from frontend.ui import _login, _interview_chat, _view_interview, _generate  # ✅ generate 추가

# ✅ 페이지 설정
st.set_page_config(page_title="AI 채용 플랫폼", page_icon="🤖", layout="wide")

# ✅ 페이지 이동 함수
def go(page):
    st.session_state.page = page
    st.rerun()

# ✅ 세션 상태 초기화
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# ✅ 현재 페이지에 따른 렌더링
page = st.session_state.page
if page == "login":
    _login.render(go)
elif page == "interview_chat":
    _interview_chat.render(go)
elif page == "view_interview":
    _view_interview.render(go)
elif page == "generate":  # ✅ 기업용 페이지 추가
    _generate.render(go)
else:
    st.error("알 수 없는 페이지입니다.")
