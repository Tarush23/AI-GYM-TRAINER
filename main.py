import streamlit as st
import os
from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults

from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css,inject_local_font
from services.persistence.exercise_repository import init_db

from dashboard.screens.user_dashboard import render_user_dashboard

def main():
    st.set_page_config(
        page_icon="🏋️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    load_css(os.path.join(os.getcwd(),"static","style.css"))
    inject_local_font(os.path.join(os.getcwd(),"static","AdobeClean.otf"),"AdobeClean")


    init_db()


    if "user_id" not in st.session_state:
        render_login_wall()
        return

    render_user_dashboard()

if __name__ == "__main__":
    main()
