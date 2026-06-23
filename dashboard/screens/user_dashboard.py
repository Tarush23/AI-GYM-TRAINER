import streamlit as st

from dashboard.components.sidebar import render_sidebar
from dashboard.components.workout_view import render_workout_screen

from services.state.session_defaults import (
    initial_session_defaults
)

import os
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline
from groq import Groq



def render_user_dashboard():

    initial_session_defaults()

    if "voice_pipeline" not in st.session_state:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            st.session_state.voice_pipeline = VoicePipeline(llm_coach,tts)
        except Exception as e:
            st.error(e)
            st.session_state.voice_pipeline = None

    username = st.session_state.get("username")

    st.header(f"hello {username}")

    render_sidebar()

    render_workout_screen()