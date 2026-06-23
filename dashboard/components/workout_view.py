import streamlit as st
from streamlit_webrtc import webrtc_streamer,WebRtcMode
from services.persistence.exercise_repository import get_users_exercises

from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update

import time
import pandas as pd



def render_workout_screen():
    workout_started = st.session_state.get("workout_started")
    user_id = st.session_state.get("user_id")
    username = st.session_state.get("username")
    st.title("AI Real-time GYM Coach")
    st.write("Real time pose detection with proactive AI voice coaching")

    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 10px dashed #444;
                border-radius: 0px; 
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
                margin-bottom: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,<br>
                    then click <strong>Start Workout</strong> to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )

        sync_metrics_update(context)

        if context.state.playing:
            time.sleep(0.25)
            st.rerun()

    st.divider()

    st.subheader("Workout history")

    response = get_users_exercises(user_id)
    if len(response)>0:
        arr = [
            {
                "Exercise":row["exercise_name"],
                "reps":row["reps"],
                "sets":row["sets"],
                "Time(sec)":row["time"],
                "Date":row["created_at"]
            }
            for row in response
        ]

        df = pd.DataFrame(arr)

        if not df.empty:
            df["Date"]=pd.to_datetime(df["Date"]).dt.date
            agg_df = df.groupby(["Exercise","Date"]).agg({
                "reps":"sum",
                "sets":"sum",
                "Time(sec)":"sum"
            }).reset_index()
            agg_df.index += 1
            st.table(agg_df)
            print(agg_df)
    else:
        st.info("no workout history found")
    #print(response)


